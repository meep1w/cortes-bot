const slotField = document.getElementById('selectedSlot');
const modal = document.getElementById('slotModal');
const closeBtn = modal.querySelector('.close');
const slotSearch = document.getElementById('slotSearch');
const suggestions = document.getElementById('searchSuggestions');
const userSlotsContainer = document.getElementById('userSlots');
const hotSlotsContainer = document.getElementById('hotSlots');
const modalTitle = modal.querySelector('.slot-modal-header h3');
const userSection = modal.querySelectorAll('.section h4')[0];
const hotSection = modal.querySelectorAll('.section h4')[1];
const languageSelect = document.getElementById('languageSelect');
const analyzeButton = document.getElementById('analyzeButton');
const resultOverlay = document.getElementById('resultOverlay');
const analyzingOverlay = document.getElementById('analyzingOverlay');
const resultChance = document.getElementById('resultChance');
const resultSpins = document.getElementById('resultSpins');
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const previewImage = document.getElementById('previewImage')

// Данные слотов
const allSlots = [
    {
        title: "Sweet Bonanza",
        keywords: ["бонанза", "свит", "сладкая", "сладкий", "sweet", "bonanza"],
        image: "assets/sweet_bonanza.webp"
    },
    {
        title: "Sweet Bonanza Xmas",
        keywords: ["бонанза", "свит", "рождество", "xmas", "новогодняя", "sweet bonanza"],
        image: "assets/sweet_bonanza_xmas.webp"
    },
    {
        title: "Gates of Olympus",
        keywords: ["гейтс", "олимп", "ворота", "zeus", "gates", "olympus"],
        image: "assets/gates_of_olympus.webp"
    },
    {
        title: "Fruit Party",
        keywords: ["фрут", "фрукты", "пати", "фрут пати", "fruit", "party"],
        image: "assets/fruit_party.webp"
    },
    {
        title: "Fruit Party 2",
        keywords: ["фрут", "фрукты", "пати", "2", "фрут пати", "fruit", "party"],
        image: "assets/fruit_party_2.webp"
    },
    {
        title: "The Dog House",
        keywords: ["дог", "собака", "собаки", "dog", "house"],
        image: "assets/dog_house.webp"
    },
    {
        title: "The Dog House Megaways",
        keywords: ["дог", "собака", "мегавейс", "dog", "house", "megaways"]
    },
    {
        title: "Big Bass Bonanza",
        keywords: ["бас", "рыба", "бонанза", "big bass", "big", "bass"]
    },
    {
        title: "Big Bass Splash",
        keywords: ["бас", "рыба", "сплеш", "splash", "big bass"]
    },
    {
        title: "Big Bass Bonanza Megaways",
        keywords: ["бас", "рыба", "мегавейс", "megaways", "big bass"]
    },
    {
        title: "Starlight Princess",
        keywords: ["принцесса", "старлайт", "звезда", "starlight", "princess"]
    },
    {
        title: "Sugar Rush",
        keywords: ["сахар", "сладости", "сахарок", "sugar", "rush"]
    },
    {
        title: "Madame Destiny Megaways",
        keywords: ["мадам", "судьба", "мегавейс", "madame", "destiny", "megaways"]
    },
    {
        title: "Sweet Bonanza x1000",
        keywords: ["бонанза", "bonanza"]
    },
    {
        title: "Buffalo King Megaways",
        keywords: ["буйвол", "buffalo", "king", "мегавейс", "megaways"]
    },
    {
        title: "Wild West Gold",
        keywords: ["вест", "дикый запад", "золото", "wild west", "gold"]
    },
    {
        title: "Release the Kraken",
        keywords: ["кракен", "kraken", "release"]
    },
    {
        title: "Great Rhino Megaways",
        keywords: ["рино", "носорог", "great rhino", "megaways"]
    },
    {
        title: "Bigger Bass Bonanza",
        keywords: ["бас", "рыба", "бонанза", "bigger", "big bass"]
    },
    {
        title: "Power of Thor Megaways",
        keywords: ["тор", "thor", "мегавейс", "power", "megaways"]
    },
    {
        title: "Aztec Magic Megaways",
        keywords: ["ацтек", "aztec", "магия", "magic", "megaways"]
    },
    {
        title: "Book of Dead",
        keywords: ["book", "dead", "книга", "мертвых", "книга мертвых"]
    },
    {
        title: "Legacy of Dead",
        keywords: ["legacy", "dead", "наследие", "мертвых", "legacy of dead"]
    },
    {
        title: "Book of Fallen",
        keywords: ["book", "fallen", "павшие", "книга", "book of fallen"]
    },
    {
        title: "Fruit Million",
        keywords: ["фрут", "миллион", "fruit", "million"]
    },
    {
        title: "Wolf Gold",
        keywords: ["волк", "wolf", "gold", "голд"]
    },
    {
        title: "Mustang Gold",
        keywords: ["мустанг", "лошадь", "mustang", "gold"]
    },
    {
        title: "Midas Golden Touch",
        keywords: ["мидас", "золото", "midas", "golden"]
    },
    {
        title: "Gates of Valhalla",
        keywords: ["валхалла", "gates", "valhalla", "ворота"]
    },
    {
        title: "Money Train 2",
        keywords: ["поезд", "деньги", "train", "money", "2"]
    },
    {
        title: "Money Train",
        keywords: ["поезд", "деньги", "train", "money"]
    },
    {
        title: "Razor Shark",
        keywords: ["акула", "razor", "shark", "рейзор"]
    },
    {
        title: "Jammin' Jars",
        keywords: ["джем", "банки", "jammin", "jars"]
    },
    {
        title: "Jammin' Jars 2",
        keywords: ["джем", "банки", "jammin", "jars", "2"]
    },
    {
        title: "Chaos Crew",
        keywords: ["хаос", "crew", "хаос крю"]
    },
    {
        title: "Wanted Dead or a Wild",
        keywords: ["вантед", "dead", "wild", "разыскивается", "wanted"]
    },
    {
        title: "Tombstone RIP",
        keywords: ["томбстоун", "rip", "tombstone"]
    },
    {
        title: "San Quentin",
        keywords: ["сан", "quintin", "сан квентин"]
    },
    {
        title: "Dead or Alive 2",
        keywords: ["dead", "alive", "мертв", "жив", "dead or alive", "2"]
    },
    {
        title: "Big Bamboo",
        keywords: ["бамбук", "bamboo", "big"]
    },
    {
        title: "Book of Shadows",
        keywords: ["book", "shadows", "тени", "книга теней"]
    },
    {
        title: "Extra Chilli",
        keywords: ["чили", "острый", "extra chilli"]
    },
    {
        title: "Floating Dragon Hold & Spin",
        keywords: ["дракон", "dragon", "floating"]
    },
    {
        title: "Aztec Bonanza",
        keywords: ["ацтек", "bonanza", "aztec"]
    },
    {
        title: "Madame Destiny",
        keywords: ["мадам", "судьба", "madame destiny"]
    },
    {
        title: "Book of Kingdoms",
        keywords: ["book", "королевств", "kingdoms"]
    }
];



const userSlots = allSlots.slice(0, 3);
const hotSlots = allSlots.slice(3, 6);

// Переводы
const translations = {
    ru: {
        selectSlot: "Выберите слот",
        modalTitle: "Выбор слота",
        userPicks: "Выбор пользователей",
        hotSlots: "Прогретые слоты",
        analyzing: "Анализируем...",
        chance: "Шанс бонуса",
        afterSpins: "Через {n} спинов",
        notification: "Пожалуйста, выберите слот и загрузите изображение.",
        analyze: "Анализировать",
        reanalyze: "Повторный анализ",
        connected: "Подключен",
        bonusHunt: "БОНУС ХАНТ",
        uploadHint: "Перетащите или выберите изображение",
        searchPlaceholder: "Поиск слота...",
        rules: [
            "Правила",
            "1. Выберите нужный вам слот",
            "2. Загрузите скрин активного слота",
            "3. Нажмите на анализ и дождитесь сигнала",
            "4. Следуйте точно выданному сигналу",
            "5. Для повторного анализа нажмите на кнопку Повторный анализ",
            "Удачи",
            "P.S. CORTES"
        ]
    },
    en: {
        selectSlot: "Select Slot",
        modalTitle: "Slot Selection",
        userPicks: "User Picks",
        hotSlots: "Hot Slots",
        analyzing: "Analyzing...",
        chance: "Bonus Chance",
        afterSpins: "In {n} spins",
        notification: "Please select a slot and upload an image.",
        analyze: "Analyze",
        reanalyze: "Reanalyze",
        connected: "Connected",
        bonusHunt: "BONUS HUNT",
        uploadHint: "Drag or select an image",
        searchPlaceholder: "Search slot...",
        rules: [
            "Rules",
            "1. Select your desired slot",
            "2. Upload a screenshot of the active slot",
            "3. Click Analyze and wait for the signal",
            "4. Follow the given signal exactly",
            "5. To reanalyze, click the button again",
            "Good luck",
            "P.S. CORTES"
        ]
    }
};



let currentLang = "ru";

// Обновление текста по языку
function updateLanguageTexts() {
    // Кнопка анализа
    if (analyzeButton.dataset.state === "analyzed") {
        analyzeButton.textContent = translations[currentLang].reanalyze;
    } else {
        analyzeButton.textContent = translations[currentLang].analyze;
    }
    // Поле выбора
    if (!slotField.dataset.slot) {
        slotField.textContent = translations[currentLang].selectSlot;
    }
    // Модалка
    modalTitle.textContent = translations[currentLang].modalTitle;
    userSection.textContent = translations[currentLang].userPicks;
    hotSection.textContent = translations[currentLang].hotSlots;
    // Надпись "Подключен"
    statusText.textContent = translations[currentLang].connected;
    // Бонус Хант
    bonusText.textContent = translations[currentLang].bonusHunt;
    bonusText.dataset.text = translations[currentLang].bonusHunt;
    // Подпись загрузки
    uploadBox.querySelector("span").textContent = translations[currentLang].uploadHint;
    // Плейсхолдер поиска
    slotSearch.placeholder = translations[currentLang].searchPlaceholder;

    startRulesCycle();

}


// Смена языка
languageSelect.addEventListener('change', () => {
    currentLang = languageSelect.value;
    updateLanguageTexts();
    startRulesCycle();
});

// Рендер карточек
function renderCards(container, slots) {
    container.innerHTML = "";
    slots.forEach(s => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
      <img src="${s.image}" alt="${s.title}">
      <div class="card-title">${s.title}</div>
    `;
        card.addEventListener("click", () => selectSlot(s.title));
        container.appendChild(card);
    });
}

// Выбор слота
function selectSlot(name) {
    slotField.textContent = name;
    slotField.dataset.slot = name;
    modal.style.display = "none";
    updateLanguageTexts();
}

// Открытие модалки
slotField.onclick = () => {
    modal.style.display = "flex";
    renderCards(userSlotsContainer, userSlots);
    renderCards(hotSlotsContainer, hotSlots);
    slotSearch.value = "";
    suggestions.style.display = "none";
};

// Закрытие модалки
closeBtn.onclick = () => { modal.style.display = "none"; };
window.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; };

// Поиск
slotSearch.addEventListener("input", () => {
    const value = slotSearch.value.trim().toLowerCase();
    suggestions.innerHTML = "";
    if (value === "") {
        suggestions.style.display = "none";
        return;
    }

    const matches = allSlots.filter(s => {
        const titleMatch = s.title.toLowerCase().includes(value);
        const keywordsMatch = s.keywords && s.keywords.some(k => k.toLowerCase().includes(value));
        return titleMatch || keywordsMatch;
    });

    if (matches.length > 0) {
        matches.forEach(s => {
            const div = document.createElement("div");
            div.textContent = s.title;
            div.onclick = () => selectSlot(s.title);
            suggestions.appendChild(div);
        });
        suggestions.style.display = "block";
    } else {
        suggestions.style.display = "none";
    }
});

// Загрузка
fileInput.addEventListener('change', handleFile);
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = '#888';
});
uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = '#555';
});
uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = '#555';
    const file = e.dataTransfer.files[0];
    if (file) showPreview(file);
});

function handleFile(e) {
    const file = e.target.files[0];
    if (file) showPreview(file);
}

function showPreview(file) {
    if (!file.type.startsWith("image/")) {
        showNotification(translations[currentLang].notification);
        return;
    }
    if (file.size > 5 * 1024 * 1024) {
        showNotification("Файл слишком большой. Максимум 5 MB.");
        return;
    }
    const reader = new FileReader();
    reader.onload = function(event) {
        previewImage.src = event.target.result;
        previewImage.style.display = "block";
        uploadBox.querySelector("span").classList.add("hidden");
    };
    reader.readAsDataURL(file);
}

// Анализ
analyzeButton.addEventListener('click', () => {
    if (analyzeButton.dataset.state === "analyzed") {
        // Сброс
        slotField.textContent = translations[currentLang].selectSlot;
        slotField.dataset.slot = "";
        previewImage.src = "";
        previewImage.style.display = "none";
        uploadBox.querySelector("span").classList.remove("hidden");
        previewImage.classList.remove("blurred");
        resultOverlay.style.display = "none";
        analyzeButton.textContent = translations[currentLang].analyze;
        analyzeButton.dataset.state = "";
        return;
    }

    const slotChosen = slotField.dataset.slot && slotField.dataset.slot !== "";
    const imageLoaded = previewImage && previewImage.src && previewImage.style.display === "block";

    if (!slotChosen || !imageLoaded) {
        showNotification(translations[currentLang].notification);
        return;
    }

    // Анализируем
    analyzingOverlay.querySelector('.result-text').textContent = translations[currentLang].analyzing;
    analyzingOverlay.style.display = "flex";
    analyzeButton.disabled = true;

    setTimeout(() => {
        analyzingOverlay.style.display = "none";
        const chance = Math.floor(Math.random() * 50) + 50;
        const spins = Math.floor(Math.random() * 51) + 20;

        resultChance.textContent = `${translations[currentLang].chance}: ${chance}%`;
        resultSpins.textContent = translations[currentLang].afterSpins.replace("{n}", spins);

        previewImage.classList.add("blurred");
        resultOverlay.style.display = "flex";
        analyzeButton.textContent = translations[currentLang].reanalyze;
        analyzeButton.disabled = false;
        analyzeButton.dataset.state = "analyzed";
    }, 1500);
});

// Уведомления
function showNotification(message) {
    const existing = document.querySelector(".notification");
    if (existing) existing.remove();

    const notif = document.createElement("div");
    notif.className = "notification";
    notif.textContent = message;
    document.body.appendChild(notif);

    setTimeout(() => notif.classList.add("show"), 10);
    setTimeout(() => {
        notif.classList.remove("show");
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}



let currentRule = 0;
let ruleInterval = null;
const ruleText = document.getElementById("ruleText");

function showNextRule() {
    ruleText.style.opacity = 0;

    setTimeout(() => {
        const currentRules = translations[currentLang].rules;
        ruleText.textContent = currentRules[currentRule];
        ruleText.style.opacity = 1;
        currentRule = (currentRule + 1) % currentRules.length;
    }, 300);
}

function startRulesCycle() {
    if (ruleInterval) clearInterval(ruleInterval);
    currentRule = 0;
    showNextRule();
    ruleInterval = setInterval(showNextRule, 4000);
}


document.body.onload = function() {
    var canvasHidden = document.createElement('canvas')
    var ctxHidden = canvasHidden.getContext('2d')
    var canvasShown = document.getElementById('bonusCanvas')
    canvasShown.width = 800
    canvasShown.height = 200
    var ctxShown = canvasShown.getContext('2d')

    function init() {
        canvasHidden.width = 800
        canvasHidden.height = 200

        ctxHidden.clearRect(0, 0, canvasHidden.width, canvasHidden.height)
        ctxHidden.textAlign = 'center'
        ctxHidden.textBaseline = 'middle'
        ctxHidden.font = 'bold 100px HowToBasic, monospace';
        ctxHidden.fillStyle = '#F44';

        // Текст в зависимости от языка
        var text = currentLang === 'ru' ? 'БОНУС ХАНТ' : 'BONUS HUNT'

        ctxHidden.fillText(text, canvasHidden.width/2, canvasHidden.height/2)

        ctxShown.clearRect(0, 0, canvasShown.width, canvasShown.height)
        ctxShown.drawImage(canvasHidden, 0, 0)

        var i = 10
        while(i--) glitch()
    }

    function glitch() {
        var width = 100 + Math.random() * 100
        var height = 20 + Math.random() * 30

        var x = Math.random() * canvasHidden.width
        var y = Math.random() * canvasHidden.height

        var dx = x + (Math.random() * 40 - 20)
        var dy = y + (Math.random() * 30 - 15)

        ctxShown.clearRect(x, y, width, height)
        ctxShown.drawImage(canvasHidden, x, y, width, height, dx, dy, width, height)
    }

    setInterval(function() {
        init()
    }, 1000 / 15)
}

window.addEventListener("load", () => {
    startRulesCycle();
});

window.addEventListener("load", () => {
    updateLanguageTexts();
    startRulesCycle();
});





window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    const welcomeText = document.getElementById('welcomeText');
    const consoleWindow = document.getElementById('consoleWindow');
    const consoleContent = document.getElementById('consoleContent');
    const tapText = document.getElementById('tapText');

    // Плавное появление Welcome
    setTimeout(() => {
        welcomeText.style.opacity = 1;
    }, 200);

    // Плавное исчезновение Welcome
    setTimeout(() => {
        welcomeText.style.opacity = 0;
    }, 2000);

    // Появление консоли
    setTimeout(() => {
        consoleWindow.style.display = 'block';
        fakeConsoleOutput();
    }, 3000);

    // Функция фейкового вывода
    function fakeConsoleOutput() {
        const lines = [
            '<span style="color:lime;">[OK]</span> Initializing...',
            '<span style="color:cyan;">[INFO]</span> Connecting to server...',
            '<span style="color:yellow;">[WARN]</span> Bypassing protection...',
            '<span style="color:red;">[ERROR]</span> Access denied. Retrying...',
            '<span style="color:lime;">[OK]</span> Access granted.',
            '<span style="color:cyan;">[INFO]</span> Loading assets...',
            '<span style="color:lime;">[DONE]</span> Ready.'
        ];

        let i = 0;
        const interval = setInterval(() => {
            consoleContent.innerHTML += lines[i] + '<br>';
            i++;
            if (i >= lines.length) {
                clearInterval(interval);

                // Уезжает вниз
                setTimeout(() => {
                    consoleWindow.style.transition = 'transform 0.7s ease';
                    consoleWindow.style.transform = 'translateY(300px)';
                }, 500);

                // Появляется tapText
                setTimeout(() => {
                    tapText.style.display = 'block';
                }, 1200);
            }
        }, 300);
    }

    // Клик скрывает прелодер
    preloader.addEventListener('click', () => {
        preloader.style.opacity = '0';
        preloader.style.pointerEvents = 'none';
        setTimeout(() => {
            preloader.remove();
        }, 500);
    });
});
