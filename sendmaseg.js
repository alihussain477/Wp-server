const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const path = require("path");

const sender = process.argv[2];
const target = process.argv[3];
const message = process.argv[4];
const delay = parseInt(process.argv[5]) * 1000;

const sessionPath = path.join(__dirname, "sessions", sender);

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function start() {
    const { state, saveCreds } = await useMultiFileAuthState(sessionPath);
    const sock = makeWASocket({ auth: state });
    sock.ev.on("creds.update", saveCreds);

    await sleep(delay);
    await sock.sendMessage(target + "@s.whatsapp.net", { text: message });
    console.log("Message sent!");
}
start();
