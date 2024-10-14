import fs from 'fs';


const CKRCsv = fs.readFileSync('./data/csv/Course - Knowledge Points - Related Courses.csv', 'utf8');
const CKRArray = CKRCsv.split('\n')
CKRArray.shift();
CKRArray.pop();
const CKR = {};
CKRArray.forEach((line) => {
    console.log(line);
    const firstDotindex = line.indexOf(',');
    const secondDotIndex = line.indexOf(',', firstDotindex + 1);
    const name = line.substring(firstDotindex+1, secondDotIndex);
    const RelatedCourses = line.substring(secondDotIndex + 1);
    // CKR[name] = RelatedCourses.match(/\"(<>.*)\"/g)[0].split(',')
    CKR[name] = [...RelatedCourses.matchAll(/\"(?<CONTENT>.*?)\"/g)][0].groups.CONTENT.split(',')

})
fs.writeFileSync('./data/json/CK.json', JSON.stringify(CKR, null, 2));