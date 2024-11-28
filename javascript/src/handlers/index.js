// src/handlers/index.js
const exampleHandler = (request, h) => {
    return h.response({ message: 'Hello from the handler!' }).code(200);
};

module.exports = {
    exampleHandler,
};