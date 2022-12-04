import { useState, useEffect } from "react";
import { Socket } from "socket.io-client";

type callbackType = (data: any) => void;

export function useRasaClient(socket: Socket, onBotUttered: callbackType) {
  const [isConnected, setIsConnected] = useState(socket.connected);

  useEffect(() => {
    socket.on("connect", () => {
      setIsConnected(true);
    });

    socket.on("disconnect", () => {
      setIsConnected(false);
    });

    socket.on("bot_uttered", onBotUttered);

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("bot_uttered");
    };
  }, []);

  const userUtter = (message: string) => {
    socket.emit("user_uttered", { message: message });
  };

  return [isConnected, userUtter] as const;
}
