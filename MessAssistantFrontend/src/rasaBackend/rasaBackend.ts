import { io } from "socket.io-client";

export function getSocket() {
  return io("http://localhost:5005");
}
