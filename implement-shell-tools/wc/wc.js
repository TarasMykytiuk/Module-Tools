import process from "node:process";
import { promises as fs } from "node:fs";

const argv = process.argv.slice(2, process.argv.length);
let flag = '';
const paths = [];
let dir = '';
let ending = '';
for (let i = 0; i < argv.length; i++) {
    if (argv[i][0] == "-") {
        flag = argv[i];
    } else {
        paths.push(argv[i]);
    }
}

if (paths.length > 0) {
    dir = paths[0].slice(0, paths[0].indexOf("/"));
    ending = paths[0].slice(paths[0].indexOf("/") + 1);
};

const files = await resolveQuery(paths, dir, ending);
await logFilesInfo(files, flag);

async function resolveQuery(paths, dir, ending) {
    let files = [];
    if (paths.length > 1) {
        files = await fs.readdir(dir);
    } else {
        files = [ending];
    }
    return files;
}

async function logFilesInfo(files, flag) {
    let totalLines = 0;
    let totalWords = 0;
    let totalBytes = 0;
    let totalOutput = '';
    for (const fileName of files) {
        let fileOutput = '';
        let filePath = dir + "/" + fileName;
        let file;
        try {
            file = await fs.readFile(filePath, "utf-8");
        } catch (error) {
            console.log(error);
        }
        let linesNum = countLinesInString(file);
        let wordsNum = countWordsInString(file);
        let bytes = file.length;
        totalLines += linesNum;
        totalWords += wordsNum;
        totalBytes += bytes;
        if (flag == "-l") {
            fileOutput = linesNum + " " + filePath;
        } else if (flag == "-w") {
            fileOutput = wordsNum + " " + filePath;
        } else if (flag == '-c') {
            fileOutput = bytes + " " + filePath;
        } else {
            fileOutput = linesNum + " " + wordsNum + " " + bytes + " " + filePath;
        }
        console.log(fileOutput);
    }
    if (files.length > 1) {
        if (flag == "-l") {
            totalOutput = totalLines + " total";
        } else if (flag == "-w") {
            totalOutput = totalWords + " total";
        } else if (flag == '-c') {
            totalOutput = totalBytes + " total";
        } else {
            totalOutput = totalLines + " " + totalWords + " " + totalBytes + " total";
        }
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
    let words = str.replace(/\n/g, ' ').split(' ');
    words = words.filter((word) => {
        return (word != '')
    });
    let wordsNum = words.length;
    return wordsNum;
}
