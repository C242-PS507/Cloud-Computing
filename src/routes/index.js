// src/routes/index.js

const routes = [
    {
        method: 'GET',
        path: '/',
        handler: (request, h) => {
            return 'Welcome to the Containerized Hapi App!';
        }
    },
    // Add more routes here
];

const initRoutes = (server) => {
    routes.forEach(route => {
        server.route(route);
    });
};

module.exports = initRoutes;