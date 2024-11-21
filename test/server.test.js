const Hapi = require('@hapi/hapi');
const { expect } = require('chai');
const routes = require('../src/routes/index');

describe('API Routes', () => {
    let server;

    before(async () => {
        server = Hapi.server({
            port: 3000,
            host: 'localhost'
        });

        server.route(routes);
    });

    it('should return 200 for GET /', async () => {
        const res = await server.inject({
            method: 'GET',
            url: '/'
        });

        expect(res.statusCode).to.equal(200);
    });

});