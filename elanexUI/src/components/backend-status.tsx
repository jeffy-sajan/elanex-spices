import { useEffect, useState } from "react";

import { getHealth } from "@/lib/api";

type BackendState = "checking" | "connected" | "unavailable";

export function BackendStatus() {
  const [state, setState] = useState<BackendState>("checking");

  useEffect(() => {
    let active = true;

    getHealth()
      .then((health) => {
        if (active && health.status === "ok") {
          setState("connected");
        } else if (active) {
          setState("unavailable");
        }
      })
      .catch(() => {
        if (active) {
          setState("unavailable");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  const label = {
    checking: "API: Checking",
    connected: "API: Connected",
    unavailable: "API: Unavailable",
  }[state];

  return (
    <span aria-live="polite" title="Django backend status">
      {label}
    </span>
  );
}
