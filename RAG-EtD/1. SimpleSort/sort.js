//this scripts will filter the course with same knwoledge points.
//the same points more, the higher the score
import fs from 'fs';

const CKR = JSON.parse(fs.readFileSync('./data/json/CK.json', 'utf8'));

const CKfilter = (course) => {
    const KnowledgePonits = CKR[course];
    delete CKR[course]; // remove the course itself
    const RelatedCoursesWithPoints = {};

    for (const course in CKR) {
        const related = CKR[course];
        let score = 0;
        related.forEach((point) => {
            if (KnowledgePonits.includes(point)) {
                score++;
            }
        });
        RelatedCoursesWithPoints[course] = score;
    }
    console.log(RelatedCoursesWithPoints);
    return Object.keys(RelatedCoursesWithPoints).sort((a, b) => RelatedCoursesWithPoints[b] - RelatedCoursesWithPoints[a]);
}
//console.log(CKfilter('Web基础'));
export default CKfilter;