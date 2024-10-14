import fs from 'fs';
import path from 'path';

const table_font = ["├──", "└──", "│  "];

const DFSDir = (dir) => {
    const files = fs.readdirSync(dir);
    const filelists = [];
    const ignorelists = ['.env', '.git', 'node_modules', '__pycache__', '.gitignore'];
    for (const file of files) {
        if (ignorelists.includes(file)) {
            continue;
        }
        const filepath = path.join(dir, file);
        const stats = fs.statSync(filepath);
        if (stats.isFile()) {
            filelists.push({
                type: 'file',
                name: file
            });
        } else if (stats.isDirectory()) {
            filelists.push({
                type: 'dir',
                name: file,
                lists: DFSDir(filepath)
            });
        }
    }
    return filelists;
}

const DirJson = DFSDir('./')

console.log(JSON.stringify(DirJson, null, 2));

const buildDirMap = (dirJson, depth = 0) => {
    const start_tokens = table_font[2].repeat(depth);
    let result = ""
    dirJson.forEach((file, index) => {
        const { type, name, lists } = file;
        const isLast = index === dirJson.length - 1;
        const font = table_font[isLast ? 1 : 0];
        const nextDepth = depth + 1;
        result += `${start_tokens}${font}${name}\n`;
        if (type === 'dir') {
            result += buildDirMap(lists, nextDepth);
        }
    });
    return result;
}

console.log(buildDirMap(DirJson));