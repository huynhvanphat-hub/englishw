const fs = require('fs');

const DATA_PATH = 'c:/Project/englishw/data.json';

// Helper function to sleep
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function fetchImageForWord(wordText) {
    const encodedWord = encodeURIComponent(wordText);
    
    // Priority 1: Lexica.art
    try {
        const lexicaUrl = `https://lexica.art/api/v1/search?q=${encodedWord}`;
        const lexicaRes = await fetch(lexicaUrl);
        if (lexicaRes.ok) {
            const lexicaData = await lexicaRes.json();
            if (lexicaData.images && lexicaData.images.length > 0) {
                return { url: lexicaData.images[0].src, source: 'Lexica' };
            }
        }
    } catch (error) {
        console.log(`[Lexica] Failed for ${wordText}:`, error.message);
    }
    
    // Priority 2: Wikipedia Commons
    try {
        const wikiUrl = `https://en.wikipedia.org/w/api.php?action=query&titles=${encodedWord}&prop=pageimages&format=json&pithumbsize=400`;
        const wikiRes = await fetch(wikiUrl);
        if (wikiRes.ok) {
            const wikiData = await wikiRes.json();
            const pages = wikiData.query?.pages;
            if (pages) {
                const pageId = Object.keys(pages)[0];
                if (pageId !== '-1' && pages[pageId].thumbnail && pages[pageId].thumbnail.source) {
                    return { url: pages[pageId].thumbnail.source, source: 'Wikipedia' };
                }
            }
        }
    } catch (error) {
        console.log(`[Wikipedia] Failed for ${wordText}:`, error.message);
    }
    
    // Priority 3: Placehold.co (Fallback)
    // Replace spaces with + for the placeholder text
    const textParam = encodeURIComponent(wordText.replace(/ /g, '+'));
    return { url: `https://placehold.co/400x300/e2e8f0/475569?text=${textParam}`, source: 'Placehold.co' };
}

async function main() {
    console.log('Đang đọc dữ liệu từ data.json...');
    let rawData;
    try {
        rawData = fs.readFileSync(DATA_PATH, 'utf-8');
    } catch (err) {
        console.error('Không thể đọc file data.json:', err);
        return;
    }
    
    const data = JSON.parse(rawData);
    
    if (!data.topics || !Array.isArray(data.topics)) {
        console.error('Định dạng data.json không hợp lệ (không tìm thấy mảng topics).');
        return;
    }
    
    let totalWords = 0;
    data.topics.forEach(topic => totalWords += (topic.words ? topic.words.length : 0));
    console.log(`Bắt đầu quét tổng cộng ${totalWords} từ vựng...\n`);
    
    let processed = 0;
    
    for (const topic of data.topics) {
        if (!topic.words) continue;
        
        for (const wordObj of topic.words) {
            processed++;
            const wordText = wordObj.word;
            console.log(`[${processed}/${totalWords}] Đang tìm ảnh cho từ: "${wordText}"...`);
            
            const result = await fetchImageForWord(wordText);
            wordObj.image_url = result.url;
            console.log(`    -> Đã lấy ảnh từ [${result.source}]`);
            
            // Sleep để tránh rate limit
            await sleep(800); 
        }
    }
    
    console.log('\nĐang lưu lại data.json...');
    fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2), 'utf-8');
    console.log('Hoàn thành cập nhật 100% hình ảnh tĩnh cho Vocab Flow!');
}

main();
