# hizli_okuma.py

rsvp_html = r"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/localforage/1.10.0/localforage.min.js"></script>

<div class="nav-bar">
    <button class="back-btn" onclick="goHome()">← Ana Menü</button>
    <div class="tag" style="margin:0; color:var(--accent);">RSVP Okuyucu</div>
</div>

<div class="dt-header" style="margin-bottom: 20px;">
    <h1 style="font-size: 36px; font-weight: 900;">ODAK <span style="color:var(--accent);">MODU</span></h1>
    <div style="color: var(--dim); font-size: 14px; letter-spacing: 1px;">Mobil Veritabanı (IndexedDB) Aktif</div>
</div>

<div class="card" style="display: flex; flex-direction: column; align-items: center; padding: 40px 20px;">
    
    <div id="rsvp-reader-box" style="width: 100%; height: 120px; background: var(--bg); border: 2px solid var(--border); border-radius: 8px; display: flex; align-items: center; position: relative; overflow: hidden; margin-bottom: 20px;">
        <div style="position: absolute; left: 50%; width: 2px; height: 15px; background-color: rgba(232,160,32,0.5); top: 0; transform: translateX(-50%);"></div>
        <div style="position: absolute; left: 50%; width: 2px; height: 15px; background-color: rgba(232,160,32,0.5); bottom: 0; transform: translateX(-50%);"></div>
        
        <div id="rsvp-word-container" style="display: flex; width: 100%; font-size: clamp(28px, 6vw, 42px); font-family: var(--mono); color: var(--text);">
            <div id="rsvp-left" style="flex: 1; text-align: right;"></div>
            <div id="rsvp-pivot" style="color: var(--accent); font-weight: bold;">Hazır</div>
            <div id="rsvp-right" style="flex: 1; text-align: left;"></div>
        </div>
    </div>

    <div style="display: flex; gap: 15px; justify-content: center; align-items: center; margin-bottom: 20px; width: 100%; flex-wrap: wrap;">
        <button id="btn-page-prev" class="btn-primary" style="padding: 8px 15px; font-size: 12px; background: #333; color: white;">< Önceki</button>
        <div style="color: white; font-family: var(--mono); font-size: 16px; background: var(--bg); padding: 8px 15px; border-radius: 4px; border: 1px solid var(--border);">
            Sayfa: <input type="number" id="input-page" value="1" min="1" style="width: 50px; text-align: center; background: #111; color: var(--accent); border: none; font-weight: bold; padding: 2px;"> 
            / <span id="total-pages">1</span>
        </div>
        <button id="btn-page-next" class="btn-primary" style="padding: 8px 15px; font-size: 12px; background: #333; color: white;">Sonraki ></button>
    </div>

    <div style="display: flex; gap: 15px; width: 100%; justify-content: center; margin-bottom: 25px;">
        <button class="btn-primary" id="btn-rsvp-play" onclick="toggleRSVP()" style="flex: 1; max-width: 150px;">BAŞLAT</button>
        <button class="btn-primary" onclick="resetRSVP()" style="flex: 1; max-width: 150px; background: var(--dim);">BAŞA SAR</button>
    </div>
    
    <div id="library-section" style="margin-top: 15px; padding: 20px; border-top: 2px solid var(--accent); width: 100%;">
        <h3 style="color: var(--accent); margin-bottom: 15px;">Kütüphanem</h3>
        <ul id="library-list" style="list-style-type: none; padding: 0;"></ul>

        <div style="margin-top: 30px; background: rgba(78,195,247,0.05); border: 1px solid rgba(78,195,247,0.2); padding: 15px; border-radius: 6px;">
            <h4 style="margin-bottom: 10px; color: var(--accent2);">📚 Dosya Yükle (.pdf / .epub)</h4>
            
            <button id="btn-native-pick" class="btn-primary" style="background: var(--panel); border: 1px solid var(--accent2); color: var(--accent2); width: 100%; margin-bottom: 10px;" onclick="window.location.href='pythonista://pickfile'">📂 CİHAZDAN DOSYA SEÇ</button>
            
            <div id="selected-file-name" style="margin-bottom: 10px; color: white; text-align: center; font-size: 14px;"></div>
            
            <button id="btn-process-file" class="btn-primary" style="background: var(--dim); width: 100%;" disabled>DOSYAYI İŞLE VE EKLE</button>
            <div id="process-status" style="margin-top: 10px; font-size: 12px; color: var(--dim); text-align: center; font-family: var(--mono);"></div>
        </div>
    </div>

    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; width: 100%; background: var(--bg); padding: 15px; border-radius: 8px; border: 1px solid var(--border); margin-top: 20px;">
        <label for="rsvp-wpm-slider" style="font-family: var(--mono); color: var(--dim);">HIZ:</label>
        <input type="range" id="rsvp-wpm-slider" min="100" max="1000" step="25" value="300" style="flex: 1; max-width: 200px; accent-color: var(--accent);">
        <span id="rsvp-wpm-display" style="font-family: var(--mono); font-size: 20px; color: var(--accent); width: 45px; text-align: right; font-weight: bold;">300</span>
        <span style="font-family: var(--sans); font-size: 14px; color: var(--dim);">WPM</span>
    </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.5/jszip.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/epubjs/dist/epub.min.js"></script>
"""

rsvp_js = r"""
const rsvpRawText = "IndexedDB motoru devrede! Artık mobil uygulamaya geçtiğinde işletim sistemi verilerini silemeyecek. Kütüphanen cihazın derinliklerine güvenle kaydediliyor.";
let normalizedText = rsvpRawText.normalize ? rsvpRawText.normalize('NFC') : rsvpRawText;
let rsvpWords = normalizedText.split(/\s+/);
let rsvpIndex = 0; let rsvpPlaying = false; let rsvpWpm = 300; let rsvpTimer = null;
let pageMap = [0]; 

let library = [];
let currentBookId = null;

// localForage (IndexedDB) Yapılandırması
localforage.config({
    name: 'MuhendislikPortali',
    storeName: 'rsvp_library_db',
    driver: localforage.LOCALSTORAGE 
});

const elRsvpLeft = document.getElementById("rsvp-left"); 
const elRsvpPivot = document.getElementById("rsvp-pivot"); 
const elRsvpRight = document.getElementById("rsvp-right"); 
const elRsvpPlayBtn = document.getElementById("btn-rsvp-play"); 
const elRsvpWpmSlider = document.getElementById("rsvp-wpm-slider"); 
const elRsvpWpmDisplay = document.getElementById("rsvp-wpm-display");
const elInputPage = document.getElementById("input-page");
const elTotalPages = document.getElementById("total-pages");

if(elRsvpWpmSlider){ 
    elRsvpWpmSlider.addEventListener("input", (e) => { 
        rsvpWpm = e.target.value; 
        elRsvpWpmDisplay.textContent = rsvpWpm; 
    }); 
}

function getORPIndex(word) { 
    let len = word.length; 
    if(len <= 1) return 0; 
    if(len >= 2 && len <= 5) return 1; 
    if(len >= 6 && len <= 9) return 2; 
    if(len >= 10 && len <= 13) return 3; 
    return 4; 
}

function displayRSVPWord(word) { 
    if (!word) return; 
    let cleanWord = word.replace(/[.,!?;:()]/g, ""); 
    let pivotIndex = getORPIndex(cleanWord); 
    if(elRsvpLeft) elRsvpLeft.textContent = word.substring(0, pivotIndex); 
    if(elRsvpPivot) elRsvpPivot.textContent = word.charAt(pivotIndex); 
    if(elRsvpRight) elRsvpRight.textContent = word.substring(pivotIndex + 1); 
}

window.nextRSVPWord = function() { 
    if (rsvpIndex >= rsvpWords.length) { 
        stopRSVP(); 
        if(elRsvpPivot) elRsvpPivot.textContent = "Bitti"; 
        if(elRsvpLeft) elRsvpLeft.textContent = ""; 
        if(elRsvpRight) elRsvpRight.textContent = ""; 
        return; 
    } 
    let currentWord = rsvpWords[rsvpIndex]; 
    displayRSVPWord(currentWord); 
    
    let delayMultiplier = 1; 
    if (currentWord.endsWith('.') || currentWord.endsWith('!') || currentWord.endsWith('?')) delayMultiplier = 1.8; 
    else if (currentWord.endsWith(',')) delayMultiplier = 1.4; 
    
    rsvpIndex++; 
    if (pageMap.includes(rsvpIndex)) updatePageUI();

    let delay = (60000 / rsvpWpm) * delayMultiplier; 
    if (rsvpPlaying) rsvpTimer = setTimeout(nextRSVPWord, delay); 
}

window.toggleRSVP = function() { if (rsvpPlaying) stopRSVP(); else startRSVP(); }

window.startRSVP = function() { 
    if (rsvpIndex >= rsvpWords.length) rsvpIndex = 0; 
    rsvpPlaying = true; 
    if(elRsvpPlayBtn){ elRsvpPlayBtn.textContent = "DURDUR"; elRsvpPlayBtn.style.background = "var(--red)"; } 
    nextRSVPWord(); 
}

window.stopRSVP = function() { 
    rsvpPlaying = false; 
    if(elRsvpPlayBtn){ elRsvpPlayBtn.textContent = "BAŞLAT"; elRsvpPlayBtn.style.background = "var(--accent)"; } 
    clearTimeout(rsvpTimer); 
    saveProgress(); 
}

window.resetRSVP = function() { stopRSVP(); rsvpIndex = 0; displayRSVPWord(rsvpWords[0]); updatePageUI(); }

// --- SAYFA YÖNETİMİ ---
function getCurrentPage() {
    for (let i = pageMap.length - 1; i >= 0; i--) {
        if (rsvpIndex >= pageMap[i]) return i + 1; 
    }
    return 1;
}

function updatePageUI() {
    if(elInputPage) elInputPage.value = getCurrentPage();
}

window.goToPage = function(pageNum) {
    if (pageNum < 1) pageNum = 1;
    if (pageNum > pageMap.length) pageNum = pageMap.length;
    rsvpIndex = pageMap[pageNum - 1]; 
    displayRSVPWord(rsvpWords[rsvpIndex]);
    updatePageUI();
    saveProgress();
}

document.getElementById("btn-page-prev").addEventListener("click", () => { stopRSVP(); goToPage(getCurrentPage() - 1); });
document.getElementById("btn-page-next").addEventListener("click", () => { stopRSVP(); goToPage(getCurrentPage() + 1); });
if (elInputPage) { elInputPage.addEventListener("change", (e) => { stopRSVP(); goToPage(parseInt(e.target.value)); }); }

// --- ASENKRON KÜTÜPHANE VE HAFIZA (INDEXED-DB) ---

async function saveLibrary() { 
    await localforage.setItem('libraryData', library); 
}

async function addNewBook(title, wordsArray, pMap) { 
    const newBook = { id: Date.now().toString(), title: title, words: wordsArray, pageMap: pMap, currentIndex: 0, totalWords: wordsArray.length }; 
    library.push(newBook); 
    await saveLibrary(); 
    return newBook.id; 
}

window.loadBook = async function(bookId) { 
    const book = library.find(b => b.id === bookId); 
    if (!book) return; 
    currentBookId = bookId; 
    await localforage.setItem('currentBookId', currentBookId); 
    rsvpWords = book.words; 
    pageMap = book.pageMap || [0]; 
    rsvpIndex = book.currentIndex; 
    if (rsvpIndex >= rsvpWords.length) rsvpIndex = 0; 
    if(elTotalPages) elTotalPages.textContent = pageMap.length;
    updatePageUI();
    displayRSVPWord(rsvpWords[rsvpIndex]); 
}

async function saveProgress() { 
    if (!currentBookId) return; 
    const book = library.find(b => b.id === currentBookId); 
    if (book) { book.currentIndex = rsvpIndex; await saveLibrary(); } 
}

window.deleteBook = async function(bookId) { 
    if (!confirm("Bu metni kütüphaneden silmek istediğine emin misin?")) return; 
    library = library.filter(b => b.id !== bookId); 
    await saveLibrary(); 
    if (currentBookId === bookId) { 
        currentBookId = null; 
        await localforage.removeItem('currentBookId'); 
        rsvpWords = ["Metin", "Silindi"]; rsvpIndex = 0; pageMap = [0]; 
        displayRSVPWord("..."); elTotalPages.textContent = 1; updatePageUI();
    } 
    renderLibrary(); 
};

window.startBookFromLibrary = function(bookId) { stopRSVP(); loadBook(bookId); renderLibrary(); };

function renderLibrary() { 
    const elLibraryList = document.getElementById("library-list"); 
    if (!elLibraryList) return; 
    elLibraryList.innerHTML = ""; 
    library.forEach(book => { 
        const li = document.createElement("li"); 
        li.style.cssText = "margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; background: #222; padding: 10px; border-radius: 5px; border-left: 3px solid var(--accent);"; 
        let progress = Math.round((book.currentIndex / book.totalWords) * 100) || 0; 
        li.innerHTML = `<span style="font-size: 0.9rem; flex-grow: 1;"><strong>${book.title}</strong> <span style="color: #888;">(%${progress} - ${book.pageMap ? book.pageMap.length : 1} Sayfa)</span></span> <div style="display: flex; gap: 5px;"> <button onclick="startBookFromLibrary('${book.id}')" class="btn-primary" style="padding: 5px 10px; font-size: 0.8rem; background: var(--accent); color: black;">Yükle</button> <button onclick="deleteBook('${book.id}')" class="btn-primary" style="padding: 5px 10px; font-size: 0.8rem; background: var(--red);">Sil</button> </div>`; 
        elLibraryList.appendChild(li); 
    }); 
}

// --- DOSYA İŞLEME (PDF & EPUB) ---
const elBtnProcessFile = document.getElementById("btn-process-file");
const elStatus = document.getElementById("process-status");

let pendingFileData = null;
let pendingFileName = "";

// Python'dan fırlatılan dosyayı yakalayan köprü fonksiyonu
window.receiveFileFromPython = function(filename, b64data) {
    pendingFileName = filename;
    
    // Python'dan gelen Base64 metnini tekrar dosyaya çeviriyoruz
    const binaryString = window.atob(b64data);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    pendingFileData = bytes.buffer;
    
    // Arayüzü güncelle ve butonu aktif et
    document.getElementById("selected-file-name").textContent = "Seçilen: " + filename;
    elBtnProcessFile.disabled = false;
    elBtnProcessFile.style.background = "var(--accent2)";
    elStatus.textContent = "Dosya işlenmeye hazır. Lütfen butona basın.";
};

if (elBtnProcessFile) {
    elBtnProcessFile.addEventListener("click", async () => {
        if (!pendingFileData) { alert("Önce dosya seçin!"); return; }
        
        elStatus.textContent = "Dosya işleniyor... (Cihazın hızına göre sürebilir)";
        elBtnProcessFile.disabled = true;

        const arrayBuffer = pendingFileData;
        const fileName = pendingFileName;

        if (fileName.endsWith(".pdf") || fileName.endsWith(".PDF")) {
            try {
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
                const pdf = await pdfjsLib.getDocument({data: new Uint8Array(arrayBuffer)}).promise;
                let allWords = []; let tempPageMap = []; let count = 0;
                
                for (let i = 1; i <= pdf.numPages; i++) {
                    tempPageMap.push(count);
                    const page = await pdf.getPage(i);
                    const textContent = await page.getTextContent();
                    const pageText = textContent.items.map(item => item.str).join(' ');
                    const words = pageText.trim().split(/\s+/).filter(w => w.length > 0);
                    allWords = allWords.concat(words);
                    count += words.length;
                    elStatus.textContent = `PDF İşleniyor: Sayfa ${i} / ${pdf.numPages}`;
                }
                const newId = await addNewBook(fileName.replace(/\.[^/.]+$/, ""), allWords, tempPageMap);
                loadBook(newId);
            } catch (e) { 
                console.error(e); alert("PDF işlenirken hata oluştu!"); 
            }
        } 
        else if (fileName.endsWith(".epub") || fileName.endsWith(".EPUB")) {
            try {
                const book = ePub(arrayBuffer);
                const spine = await book.loaded.spine;
                
                let allWords = []; let tempPageMap = []; let count = 0;
                let wordsPerPage = 250; 
                
                for (const section of spine.spineItems) {
                    try {
                        const doc = await section.load(book.load.bind(book));
                        
                        let text = "";
                        // GÜVENLİK YAMASI 2.0: Sayfa formatı ne olursa olsun metni söküp al
                        if (typeof doc === "string") {
                            // Kütüphane düz metin (string) döndürdüyse HTML etiketlerini kazı
                            const tempDiv = document.createElement("div");
                            tempDiv.innerHTML = doc;
                            text = tempDiv.textContent || tempDiv.innerText || "";
                        } else if (doc) {
                            // Kütüphane XML veya HTML dosyası döndürdüyse (body yoksa bile metni al)
                            text = (doc.body ? doc.body.textContent : doc.textContent) || "";
                        }
                        
                        if (text.trim().length > 0) {
                            const words = text.trim().split(/\s+/).filter(w => w.length > 0);
                            for (let j = 0; j < words.length; j++) {
                                if (count % wordsPerPage === 0) tempPageMap.push(count);
                                allWords.push(words[j]);
                                count++;
                            }
                        }
                        section.unload(); // Hafızayı koru
                        
                    } catch (chapterErr) {
                        console.warn("Bir EPUB bölümü atlandı:", chapterErr);
                    }
                }
                
                if (allWords.length === 0) {
                    alert("Kitaptan hiç metin çıkarılamadı.");
                    elBtnProcessFile.disabled = true;
                    elBtnProcessFile.style.background = "var(--dim)";
                    return; 
                }
                
                const newId = await addNewBook(fileName.replace(/\.[^/.]+$/, ""), allWords, tempPageMap);
                loadBook(newId);
                
            } catch (e) { 
                console.error("Ana EPUB Hatası:", e); 
                alert("EPUB dosyası okunamadı! (Dosya bozuk olabilir)"); 
            }
        }

        elStatus.textContent = "İşlem Tamamlandı!";
        renderLibrary();
        
        // İşlem bitince butonu sıfırla ve kitle
        elBtnProcessFile.disabled = true;
        elBtnProcessFile.style.background = "var(--dim)";
        pendingFileData = null;
    });
}
// UYGULAMA BAŞLANGICI (Veritabanını Bekle ve Çökmeyi Önle)
async function initApp() {
    try {
        library = (await localforage.getItem('libraryData')) || [];
        currentBookId = await localforage.getItem('currentBookId') || null;
    } catch (e) {
        console.error("Hafıza Engellendi:", e);
        library = [];
        currentBookId = null;
    }
    
    renderLibrary();
    if (currentBookId) {
        await loadBook(currentBookId);
    } else {
        if (typeof elTotalPages !== 'undefined' && typeof pageMap !== 'undefined') {
            elTotalPages.textContent = pageMap.length;
        }
        displayRSVPWord(rsvpWords[0]);
    }
}

// Sistemi Başlat
initApp();
"""
