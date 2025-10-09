const redis = require("redis");
const express = require("express");

const port = 3000;

// hostname 'redis-server' will be visible on the network created by Docker Compose
const client = redis.createClient({
  host: "redis-server",
  port: 6379, // 6379 default port
});

client.set("visits", 0);

const app = express();

app.get("/", (req, res) => {
  client.get("visits", (err, reply) => {
    res.send("The number of page visits: " + reply);
    client.set("visits", parseInt(reply) + 1);
  });
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));
