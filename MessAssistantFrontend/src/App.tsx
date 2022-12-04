import { useState, MouseEventHandler } from "react";
import { Grid, GridItem, useDisclosure } from "@chakra-ui/react";
import "./App.css";
import Header from "./Header/Header";
import Footer from "./Footer/Footer";
import LoginModal from "./LoginModal/LoginModal";
import { getSocket } from "./rasaBackend/rasaBackend";
import { useRasaClient } from "./rasaBackend/hooks";
import Chat from "./Chat/Chat";

export type rasaButtonInfo = {
  title: string;
  payload: string;
  disable: boolean;
  clicked: boolean;
  onClick: (
    userUtter: (message: string) => void,
    buttonIndex: number
  ) => MouseEventHandler<HTMLButtonElement>;
};

export type chat = {
  sender: string;
  message?: string;
  time: Date;
  buttons?: rasaButtonInfo[];
  image?: string;
};

export type chatMessage = {
  sender: string;
  message: string;
  time: Date;
};

const socket = getSocket();
function App() {
  const [chats, setChats] = useState<chat[]>([]);
  const [ssid, setSsid] = useState("");
  const [verified, setVerified] = useState(false);

  const { isOpen, onOpen, onClose } = useDisclosure();

  const addChat = (chatEl: chat) =>
    setChats((prevChats) => {
      let lastChat = prevChats.at(-1);
      if (lastChat != undefined && lastChat.buttons != undefined) {
        for (let btnInfo of lastChat.buttons ?? []) btnInfo.disable = true;
        return [...prevChats.slice(0, -1), lastChat, chatEl];
      }
      return [...prevChats, chatEl];
    });

  const [isConnected, userUtter] = useRasaClient(socket, (data, ...args) => {
    if (data?.verified != undefined) {
      setVerified(data?.verified);
      if (!data?.verified) onOpen();
      return;
    }

    setChats((prevChats) => {
      const newChat: chat = { time: new Date(), sender: "bot" };
      console.log(data);
      console.log(args);
      const index = prevChats.length;
      newChat.message = data?.text;
      if (data?.attachment?.type == "image")
        newChat.image = data.attachment.payload.src;
      if (data?.quick_replies != undefined) {
        const buttons: rasaButtonInfo[] = [];
        for (const buttonInfo of data.quick_replies) {
          buttons.push({
            title: buttonInfo.title,
            disable: false,
            clicked: false,
            payload: buttonInfo.payload,
            onClick: (userUtter, buttonIndex) => (e) => {
              e.preventDefault();
              setChats((buttonPrevChats) =>
                buttonPrevChats.map((chatEl, i) =>
                  index == i
                    ? {
                        ...chatEl,
                        buttons: chatEl.buttons?.map((btnEl, j) => ({
                          ...btnEl,
                          clicked: buttonIndex === j,
                          disable: true,
                        })),
                      }
                    : chatEl
                )
              );
              userUtter(buttonInfo.payload);
            },
          });
        }
        newChat.buttons = buttons;
      }
      return [...prevChats, newChat];
    });
  });
  const sendChat = (chatEl: chatMessage) => {
    addChat(chatEl);
    userUtter(chatEl.message);
  };

  return (
    <>
      <LoginModal
        isOpen={isOpen}
        onClose={onClose}
        onOpen={onOpen}
        userUtter={userUtter}
        setSsid={setSsid}
      />
      <Grid
        templateAreas={`"header" 
                      "chat" 
                      "footer"`}
        gridTemplateRows={"5em 1fr 5em"}
        h="100%"
      >
        <GridItem area={"header"}>
          <Header />
        </GridItem>
        <GridItem
          area={"chat"}
          boxShadow="dark-lg"
          rounded="md"
          overflowY="auto"
          marginX="5%"
          padding="5%"
        >
          <Chat userUtter={userUtter} chats={chats} />
        </GridItem>
        <GridItem area={"footer"}>
          <Footer
            verified={verified}
            isConnected={isConnected}
            addChat={sendChat}
          />
        </GridItem>
      </Grid>
    </>
  );
}

export default App;
