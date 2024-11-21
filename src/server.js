const Hapi = require('@hapi/hapi');
const routes = require('./routes');
const config = require('./config');

const init = async () => {
    const server = Hapi.server({
        port: config.port,
        host: config.host,
    });

    server.route(routes);

    await server.start();
    console.log(`Server running on ${server.info.uri}`);
};

process.on('unhandledRejection', (err) => {
    console.log(err);
    process.exit(1);
});

init();