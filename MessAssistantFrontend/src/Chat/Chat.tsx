import { Box, Text, SimpleGrid, Button, Center } from "@chakra-ui/react";
import "./Chat.css";
import { useRef, useEffect } from "react";
import { chat } from "../App";

type ChatProps = {
  chats: chat[];
  userUtter: (message: string) => void;
};

function Chat({ chats, userUtter }: ChatProps) {
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chats]);

  return (
    <Box h="100%">
      <ul className="chats">
        {chats.map((chatEl, index) => (
          <li key={index}>
            <Box
              float={chatEl.sender == "bot" ? "left" : "right"}
              textAlign={chatEl.sender == "bot" ? "left" : "right"}
              boxShadow="dark-lg"
              marginBottom="5%"
              padding="2%"
              minWidth="51%"
              maxWidth="75%"
              rounded="md"
            >
              {chatEl.message}
              {chatEl.image != undefined ? <img src={chatEl.image} /> : null}
              <Text
                fontSize="xs"
                textAlign={chatEl.sender == "bot" ? "left" : "right"}
              >
                {chatEl.time.toLocaleString()}
              </Text>
            </Box>
            {chatEl.buttons == undefined ? null : (
              <SimpleGrid
                w="100%"
                minChildWidth="250px"
                spacingX="40px"
                spacingY="20px"
                marginBottom="10%"
              >
                {chatEl.buttons.map((buttonInfo, index) => (
                  <Button
                    boxShadow="dark-lg"
                    padding="2%"
                    rounded="md"
                    onClick={buttonInfo.onClick(userUtter, index)}
                    wordBreak="break-all"
                    disabled={buttonInfo.disable}
                    variant={buttonInfo.clicked ? "solid" : "outline"}
                    key={index.toString()}
                  >
                    {buttonInfo.title}
                  </Button>
                ))}
              </SimpleGrid>
            )}
          </li>
        ))}
        <Box ref={messagesEndRef} float="right" width="100%" height="1px"></Box>
      </ul>
    </Box>
  );
}

export default Chat;
