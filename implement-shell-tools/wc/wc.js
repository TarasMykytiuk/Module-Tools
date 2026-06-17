import process from "node:process";
import { promises as fs } from "node:fs";

const argv = process.argv.slice(2, process.argv.length);
const flags = [];
const paths = [];
let dir = '';
let ending = '';
for (let i = 0; i < argv.length; i++) {
    if (argv[i][0] === "-") {
        flags.push(argv[i]);
    } else {
        paths.push(argv[i]);
    }
}

if (paths.length > 0) {
    dir = paths[0].slice(0, paths[0].indexOf("/"));
    ending = paths[0].slice(paths[0].indexOf("/") + 1);
};

const files = await resolveQuery(paths, dir, ending);
await logFilesInfo(files, flags);

async function resolveQuery(paths, dir, ending) {
    let files = [];
    if (paths.length > 1) {
        files = await fs.readdir(dir);
    } else {
        files = [ending];
    }
    return files;
}

async function logFilesInfo(files, flags) {
    let totalLines = 0;
    let totalWords = 0;
    let totalBytes = 0;
    let totalOutput = '';
    for (const fileName of files) {
        let fileOutput = '';
        const filePath = dir + "/" + fileName;
        let file;
        try {
            file = await fs.readFile(filePath, "utf-8");
        } catch (error) {
            console.log(error);
        }
        const linesNum = countLinesInString(file);
        const wordsNum = countWordsInString(file);
        const bytes = Buffer.byteLength(file, "utf-8");
        totalLines += linesNum;
        totalWords += wordsNum;
        totalBytes += bytes;
        if (flags.includes("-l")) {
            fileOutput += linesNum.toString().padStart(3, " ");
        }
        if (flags.includes("-w")) {
            fileOutput += " " + wordsNum.toString().padStart(3, " ");
        }
        if (flags.includes("-c")) {
            fileOutput += " " + bytes.toString().padStart(3, " ");
        }
        fileOutput += " " + filePath;
        console.log(fileOutput);
    }
    if (files.length > 1) {
        if (flags.includes("-l")) {
            totalOutput += totalLines.toString().padStart(3, " ");
        }
        if (flags.includes("-w")) {
            totalOutput += " " + totalWords.toString().padStart(3, " ")
        }
        if (flags.includes("-c")) {
            totalOutput += " " + totalBytes.toString().padStart(3, " ");
        }
        totalOutput += " total";
        console.log(totalOutput);
    }
}

function countLinesInString(str) {
    let lines = str.split('\n');
    let linesNum = lines.length;
    if (lines[lines.length - 1] == '') {
        linesNum--;
    }
    return linesNum;
}

function countWordsInString(str) {
    if (!str.trim()) return 0;
    let words = str.trim().split(/\s+/); // now take into account any whitespaces
    return words.length;
}
