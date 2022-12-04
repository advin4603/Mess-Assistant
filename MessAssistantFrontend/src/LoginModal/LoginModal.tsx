import "./LoginModal.css";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  Input,
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  useDisclosure,
  Button,
} from "@chakra-ui/react";
import { loginBackend } from "../loginBackend/loginBackend";
import { useEffect, useState, FormEventHandler } from "react";

type LoginModalProps = {
  setSsid: (ssid: string) => void;
  userUtter: (message: string) => void;
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
};

function LoginModal({
  setSsid,
  userUtter,
  isOpen,
  onOpen,
  onClose,
}: LoginModalProps) {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    onOpen();
  }, []);

  const submit: FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const response = await loginBackend.post("/", formData);
    if (response.status == 200 && response.data.TGC !== null) {
      const ssid =
        "_" + response.data.PHPSESSID + "|" + response.data.TGC + "_";

      userUtter(`/inform_session_id{"session_id":"${ssid}"}`);
      setSsid(ssid);
      onClose();
    } else if (response.data.TGC == null) {
      setError("Invalid Username or Password");
      setIsLoading(false);
      console.log(response);
    } else {
      setError("Couldn't Log In.");
      setIsLoading(false);
      console.log(response);
    }
  };

  return (
    <Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <form onSubmit={submit}>
        <ModalContent>
          <ModalHeader>Login Using CAS credentials</ModalHeader>
          <ModalBody>
            {error !== "" ? (
              <Alert status="error">
                <AlertIcon />
                <AlertTitle>{error}</AlertTitle>
              </Alert>
            ) : null}
            <FormControl isRequired marginTop="5%">
              <FormLabel>Email address</FormLabel>
              <Input
                boxShadow="dark-lg"
                value={formData.username}
                onChange={(e) => {
                  setFormData({ ...formData, username: e.target.value });
                }}
                type="email"
              />
            </FormControl>
            <FormControl isRequired marginY="5%">
              <FormLabel>Password</FormLabel>
              <Input
                boxShadow="dark-lg"
                onChange={(e) => {
                  setFormData({ ...formData, password: e.target.value });
                }}
                value={formData.password}
                type="password"
              />
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button
              isLoading={isLoading}
              loadingText="Logging In"
              type="submit"
              boxShadow="dark-lg"
            >
              Login
            </Button>
          </ModalFooter>
        </ModalContent>
      </form>
    </Modal>
  );
}

export default LoginModal;
