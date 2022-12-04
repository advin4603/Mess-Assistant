import "./Header.css";
import {
  Center,
  Heading,
  Button,
  useColorMode,
  HStack,
  Spacer,
  IconButton,
} from "@chakra-ui/react";
import { SunIcon, MoonIcon } from "@chakra-ui/icons";

function Header() {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <HStack h="100%" w="100%" paddingX="5%">
      <Heading>Mess Assistant</Heading>
      <Spacer />
      <IconButton
        boxShadow="dark-lg"
        onClick={toggleColorMode}
        aria-label="switch theme"
        icon={colorMode == "dark" ? <MoonIcon /> : <SunIcon />}
      />
    </HStack>
  );
}

export default Header;
