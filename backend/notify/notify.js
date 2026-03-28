// iMessage alert bridge — called by Python via subprocess
// Reads TO and MESSAGE from environment variables
const { IMessageSDK } = require("@photon-ai/imessage-kit");

async function main() {
  const to = process.env.TO;
  const message = process.env.MESSAGE;
  if (!to || !message) {
    console.error("Missing TO or MESSAGE env vars");
    process.exit(1);
  }
  const sdk = new IMessageSDK();
  try {
    await sdk.send(to, message);
  } finally {
    await sdk.close();
  }
}

main().catch((e) => {
  console.error("iMessage send error:", e.message);
  process.exit(1);
});
