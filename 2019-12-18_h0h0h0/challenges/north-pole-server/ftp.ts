import { FtpSrv } from "ftp-srv";
import * as redis from "redis";
import * as fs from "fs";

import { md5 } from "./utils/crypto";

const redisClient = redis.createClient({
    host: "127.0.0.1",
    port: 6379
});

const ftpServer = new FtpSrv({
    url: `ftp://0.0.0.0:${process.env.FTP_PORT || 5001}`,
    blacklist: ["MKD", "XMKD", "RMD", "XRMD"],
    greeting: "h0h0h0",
    pasv_url: `ftp://${process.env.FTP_PASV_IP || "127.0.0.1"}`,
    pasv_min: Number(process.env.FTP_PASV_MIN || 5002),
    pasv_max: Number(process.env.FTP_PASV_MAX || 5020)
});

ftpServer.on("login", (data, resolve, reject) => {
    if (
        !/^[A-z0-9]{8,32}$/.test(data.username) ||
        !/^[A-z0-9]{8,32}$/.test(data.password)
    ) {
        reject(
            new Error(
                "Both username and password must match /^[A-z0-9]{8,32}$/ regex"
            )
        );
    } else {
        const hash = md5(
            `${data.username}_${data.password}_${process.env.SECRET}`
        );
        redisClient.exists(`${hash}_admin`, (err, reply) => {
            if (err) {
                reject(new Error(err.message));
            } else {
                const path = `${__dirname}/userdata/${
                    reply === 0 ? hash : "admin"
                }`;

                if (!fs.existsSync(path)) {
                    fs.mkdirSync(path);
                }

                resolve({
                    cwd: "/",
                    root: path
                });
            }
        });
    }
});

ftpServer
    .listen()
    .then(() =>
        console.log(
            "ftp server listening on port",
            process.env.FTP_PORT || 5001
        )
    );
