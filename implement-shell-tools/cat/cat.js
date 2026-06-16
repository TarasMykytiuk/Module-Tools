import process from "node:process";
import { promises as fs } from "node:fs";

const argv = process.argv.slice(2, process.argv.length);
const flags = [];
const paths = [];
for (let i = 0; i < argv.length; i++) {
    if (argv[i][0] == "-") {
        flags.push(argv[i]);
    } else {
        paths.push(argv[i]);
    }
}

displayFiles(paths, flags);

async function displayFiles(paths, flags) {
    let content = '';
    for (let i = 0; i < paths.length; i++) {
        try {
            content += await fs.readFile(paths[i], "utf-8");
        } catch (error) {
            console.log(error)
        }

    }

    const lines = content.split("\n");
    if (lines[lines.length - 1] == '') {
        lines.pop();
    }
    let lineNumber = 1;
    for (let i = 0; i < lines.length; i++) {
        let output = lines[i];
        if (
            (flags.includes("-n") && !flags.includes("-b")) ||
            (flags.includes("-b") && lines[i] !== "")
        ) {
            output = (lineNumber).toString().padStart(6) + "\t" + lines[i];
            lineNumber++;
        }
        console.log(output);
    }
}
