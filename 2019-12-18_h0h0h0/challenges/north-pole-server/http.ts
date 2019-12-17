import * as express from "express";
import * as bodyParser from "body-parser";
import * as session from "express-session";
import * as connectRedis from "connect-redis";
import * as redis from "redis";
import * as multer from "multer";
import * as fs from "fs";

import { md5 } from "./utils/crypto";

const app = express();
const redisStore = connectRedis(session);
const redisClient = redis.createClient({
    host: "127.0.0.1",
    port: 6379
});

app.use(
    session({
        store: new redisStore({ client: redisClient, db: 15 }),
        secret: process.env.SECRET || "h0h0h0",
        saveUninitialized: false,
        resave: false
    })
);

app.use(
    bodyParser.urlencoded({
        extended: true
    })
);

app.post(
    "/api/login",
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        if (
            !/^[A-z0-9]{8,32}$/.test(req.body.username) ||
            !/^[A-z0-9]{8,32}$/.test(req.body.password)
        ) {
            res.status(400).send(
                "Both username and password must match /^[A-z0-9]{8,32}$/ regex"
            );
        } else {
            redisClient.exists(`${req.session.hash}_admin`, (err, reply) => {
                if (err) {
                    res.status(500).send(err.message);
                } else {
                    const hash = !reply
                        ? md5(
                              `${req.body.username}_${req.body.password}_${process.env.SECRET}`
                          )
                        : "admin";

                    req.session.hash = hash;
                    const path = `${__dirname}/userdata/${hash}`;
                    if (!fs.existsSync(path)) {
                        fs.mkdirSync(path);
                    }

                    res.redirect("/upload.html");
                }
            });
        }
    }
);

app.post(
    "/api/logout",
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        req.session.destroy(() => res.redirect("/upload.html"));
    }
);

const storage = multer.memoryStorage();
const upload = multer({
    storage,
    limits: {
        fileSize: 4 * 1024 * 1024
    }
});
app.post(
    "/api/upload",
    upload.single("file"),
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        if (!req.session.hash) {
            res.status(403).send("please login");
        } else {
            const userpath = `${__dirname}/userdata/${req.session.hash}`;
            fs.writeFileSync(
                `${userpath}/${req.file.originalname.replace(/\.\./g, ".")}`,
                req.file.buffer
            );

            res.redirect("/upload.html");
        }
    }
);

app.get(
    "/api/files",
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        if (!req.session.hash) {
            res.status(403).send("please login");
        } else {
            const userpath = `${__dirname}/userdata/${req.session.hash}`;
            fs.readdir(userpath, (err, files) =>
                err ? res.status(500).send(err.message) : res.json(files)
            );
        }
    }
);

app.get(
    "/api/files/:filename",
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        if (!req.session.hash) {
            res.status(403).send("please login");
        } else {
            const userpath = `${__dirname}/userdata/${req.session.hash}`;
            res.sendFile(
                `${userpath}/${req.params.filename.replace(/\.\./g, ".")}`
            );
        }
    }
);

app.delete(
    "/api/files/:filename",
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        if (!req.session.hash) {
            res.status(403).send("please login");
        } else {
            const userpath = `${__dirname}/userdata/${req.session.hash}`;
            fs.unlinkSync(
                `${userpath}/${req.params.filename.replace(/\.\./g, ".")}`
            );
            res.status(204).send();
        }
    }
);

app.get(
    "/api/is_admin",
    (
        req: express.Request,
        res: express.Response,
        next: express.NextFunction
    ) => {
        if (!req.session.hash) {
            res.status(403).send("please login");
        } else {
            redisClient.exists(`${req.session.hash}_admin`, (err, reply) =>
                err ? res.status(500).send(err.message) : res.json(!!reply)
            );
        }
    }
);

app.use(express.static(`${__dirname}/static`));

(async () => {
    app.listen(Number(process.env.HTTP_PORT || 5000), () =>
        console.log("http server listening on", process.env.HTTP_PORT || 5000)
    );
})();
