const Koa = require('koa');

const app = new Koa();
const router = require('koa-router')();
const bodyParser = require('koa-bodyparser');

// app.use(async (ctx, next) => {
//     const start = new Date().getTime(); // 当前时间
//     await next(); // 调用下一个middleware
//     const ms = new Date().getTime() - start; // 耗费时间
//     console.log(`Time: ${ms}ms`); // 打印耗费时间
// });

app.use(async (ctx, next) => {
    console.log(`${ctx.request.method} ${ctx.request.url}...`);
    await next();
});

router.get('/hello/:name', async (ctx,netx) => {
    var name = ctx.params.name;
    ctx.response.body = `<h1>hello, ${name}!</h1>`;
})

router.get('/', async (ctx, next) => {
    ctx.response.body = '<h1>Index</h1>';
})

// app.use(async (ctx, next) => {
//     await next();
//     ctx.response.type = 'text/html';
//     ctx.response.body = '<h1>Hello, koa2!</h1>';
// });

app.use(router.routes())
app.use(bodyParser());

app.listen(9999);
console.log('app started at port 9999....');
