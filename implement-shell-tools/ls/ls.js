import process from "node:process";
import { promises as fs } from "node:fs";

const argv = process.argv.slice(2, process.argv.length);
const currentDir = './';
const flags = [];
let path = '';
for (let i = 0; i < argv.length; i++) {
    if (argv[i][0] == "-") {
        flags.push(argv[i]);
    } else {
        path = argv[i];
    }
}
if (path == '') path = currentDir;

const content = await fs.readdir(path);
const visible = content.filter((element) => {
    return element[0] === ".";
})

if (flags.includes("-1")) {
    for (let i = 0; i < content.length; i++) {
        let line = content[i];
        if (!flags.includes("-a") && line[0] == ".") continue;
        console.log(line);
    }
} else {
    console.log(content.join(" "));
}
