import "./Footer.css";
import {
  InputGroup,
  Input,
  InputLeftElement,
  InputRightElement,
  Button,
  IconButton,
  Box,
  Spinner,
  Center,
} from "@chakra-ui/react";
import { ArrowRightIcon, ChatIcon } from "@chakra-ui/icons";
import { chatMessage } from "../App";
import { ChangeEvent, useState } from "react";

type FooterProps = {
  addChat: (chatEl: chatMessage) => void;
  isConnected: boolean;
  verified: boolean;
};

function Footer({ addChat, isConnected, verified }: FooterProps) {
  const [message, setMessage] = useState("");
  const handleChange = (event: ChangeEvent<HTMLInputElement>) =>
    setMessage(event.target.value);
  return (
    <Center paddingX="5%" h="100%">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          addChat({ message, time: new Date(), sender: "user" });
          setMessage("");
        }}
      >
        <InputGroup size="lg" boxShadow="dark-lg" variant="flushed" w="100%">
          <InputLeftElement>
            {isConnected ? (
              verified ? (
                <ChatIcon color="green.400" />
              ) : (
                <ChatIcon />
              )
            ) : (
              <Spinner />
            )}
          </InputLeftElement>
          <Input
            disabled={!isConnected}
            onChange={handleChange}
            value={message}
          />
          <InputRightElement>
            <IconButton
              type="submit"
              size="sm"
              boxShadow="dark-lg"
              aria-label="Send Message"
              icon={<ArrowRightIcon />}
            />
          </InputRightElement>
        </InputGroup>
      </form>
    </Center>
  );
}

export default Footer;
