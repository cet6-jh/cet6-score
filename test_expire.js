// 测试脚本：用 CDP 直接执行 JS 检查页面状态
const http = require('http');

console.log('=== 服务器当前时间 ===');
console.log('Date.now() =', Date.now());
console.log('Math.floor(Date.now()/1000) =', Math.floor(Date.now()/1000));

console.log('\n=== 测试页面源文件 ===');
const https = require('https');
https.get('https://cet6-jh.github.io/cet6-score/', (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
        const match = body.match(/var EXPIRE_TIMESTAMP\s*=\s*(\d+)/);
        if (match) {
            const ts = parseInt(match[1]);
            const now = Math.floor(Date.now()/1000);
            console.log('EXPIRE_TIMESTAMP =', ts);
            console.log('当前时间戳 =', now);
            console.log('差值（秒） =', ts - now);
            console.log('状态:', ts > now ? '✅ 未过期' : '❌ 已过期');

            // 检查页面中"链接已过期"字符串出现次数
            const count = (body.match(/链接已过期/g) || []).length;
            console.log('\n页面源文件中"链接已过期"出现次数:', count);
            console.log('（说明：脚本里有硬编码的过期页HTML字符串，所以匹配是正常的）');

            // 真正判断：title 是否是 "链接已过期"
            const titleMatch = body.match(/<title>([^<]+)<\/title>/g);
            console.log('\n所有 title 标签:', titleMatch);
        }
    });
}).on('error', console.error);