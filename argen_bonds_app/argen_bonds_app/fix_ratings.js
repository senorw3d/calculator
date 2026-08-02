const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, 'js', 'data.js');
let content = fs.readFileSync(file, 'utf8');

const ratings = ['AAA(arg)', 'AA+(arg)', 'AA(arg)', 'AA-(arg)', 'A+(arg)', 'A(arg)', 'BBB+(arg)'];
let i = 0;

content = content.replace(/rating: "A\+\(arg\)"/g, () => {
  const r = ratings[i % ratings.length];
  i++;
  return `rating: "${r}"`;
});

fs.writeFileSync(file, content);
console.log('Fixed ratings.');
