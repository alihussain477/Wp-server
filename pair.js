const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const path = require("path");

const sender = process.argv[2];
const sessionPath = path.join(__dirname, "sessions", sender);

async function start() {
    const { state, saveCreds } = await useMultiFileAuthState(sessionPath);
    const sock = makeWASocket({ auth: state });
    sock.ev.on("creds.update", saveCreds);
    sock.ev.on("connection.update", ({ connection, qr }) => {
        if (qr) console.log("Scan QR:\n", qr);
    });
}
start();
