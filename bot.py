import os
import telebot
from telebot import types

# ==========================================
# 1. НАСТРОЙКИ И ТОКЕНЫ
# ==========================================
TOKEN = "8907239874:AAHb99IIunyP9TrZzmjozImbjKCI9XJCp_o"
SUPPORT_USERNAME = "@borisovmukuta"  # Замените на ваш юзернейм в Telegram

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения выбранного языка пользователей {chat_id: 'ru' / 'ua' / 'en'}
user_languages = {}

# ==========================================
# 2. АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ФАЙЛА СКРИПТА
# ==========================================
LUA_CODE = """local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local RunService = game:GetService("RunService")
local Camera = workspace.CurrentCamera

-- Настройки функций
local aimbotEnabled = false
local espEnabled = false

-- Создаем интерфейс
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "XenoCheatMenu"
ScreenGui.Parent = LocalPlayer:WaitForChild("PlayerGui")
ScreenGui.ResetOnSpawn = false

local MainFrame = Instance.new("Frame")
MainFrame.Size = UDim2.new(0, 240, 0, 320)
MainFrame.Position = UDim2.new(0.1, 0, 0.2, 0)
MainFrame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
MainFrame.BorderSizePixel = 2
MainFrame.BorderColor3 = Color3.fromRGB(255, 0, 0)
MainFrame.Active = true
MainFrame.Draggable = true
MainFrame.Parent = ScreenGui

local Title = Instance.new("TextLabel")
Title.Size = UDim2.new(1, 0, 0, 35)
Title.Text = "Blox Strike: Xeno Menu"
Title.TextColor3 = Color3.fromRGB(255, 255, 255)
Title.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
Title.Font = Enum.Font.SourceSansBold
Title.TextSize = 18
Title.Parent = MainFrame

-- Функция создания кнопок
local function createButton(text, yPos, color, parent)
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0.9, 0, 0, 35)
    btn.Position = UDim2.new(0.05, 0, 0, yPos)
    btn.Text = text
    btn.BackgroundColor3 = color
    btn.TextColor3 = Color3.fromRGB(255, 255, 255)
    btn.Font = Enum.Font.SourceSansBold
    btn.TextSize = 16
    btn.Parent = parent
    return btn
end

-- ==================== ВХ (ESP) ====================
local BtnESP = createButton("ВХ (ESP): ВЫКЛ", 45, Color3.fromRGB(60, 60, 60), MainFrame)

local function updateESP()
    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and player.Character then
            local highlight = player.Character:FindFirstChild("WallhackESP")
            if espEnabled then
                if not highlight then
                    highlight = Instance.new("Highlight")
                    highlight.Name = "WallhackESP"
                    highlight.FillColor = Color3.fromRGB(255, 0, 0)
                    highlight.OutlineColor = Color3.fromRGB(255, 255, 255)
                    highlight.FillTransparency = 0.5
                    highlight.DepthMode = Enum.HighlightDepthMode.AlwaysOnTop
                    highlight.Parent = player.Character
                end
            else
                if highlight then highlight:Destroy() end
            end
        end
    end
end

BtnESP.MouseButton1Click:Connect(function()
    espEnabled = not espEnabled
    BtnESP.Text = espEnabled and "ВХ (ESP): ВКЛ" or "ВХ (ESP): ВЫКЛ"
    BtnESP.BackgroundColor3 = espEnabled and Color3.fromRGB(0, 150, 0) or Color3.fromRGB(60, 60, 60)
end)

RunService.RenderStepped:Connect(function()
    if espEnabled then updateESP() end
end)

-- ==================== АИМБОТ ====================
local BtnAimbot = createButton("АИМБОТ: ВЫКЛ", 85, Color3.fromRGB(60, 60, 60), MainFrame)

local function getNearestTarget()
    local nearestTarget = nil
    local shortestDistance = math.huge

    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("Head") then
            local humanoid = player.Character:FindFirstChild("Humanoid")
            if humanoid and humanoid.Health > 0 then
                local distance = (player.Character.Head.Position - Camera.CFrame.Position).Magnitude
                if distance < shortestDistance then
                    shortestDistance = distance
                    nearestTarget = player.Character.Head
                end
            end
        end
    end
    return nearestTarget
end

BtnAimbot.MouseButton1Click:Connect(function()
    aimbotEnabled = not aimbotEnabled
    BtnAimbot.Text = aimbotEnabled and "АИМБОТ: ВКЛ" or "АИМБОТ: ВЫКЛ"
    BtnAimbot.BackgroundColor3 = aimbotEnabled and Color3.fromRGB(150, 0, 0) or Color3.fromRGB(60, 60, 60)
end)

RunService.RenderStepped:Connect(function()
    if aimbotEnabled then
        local target = getNearestTarget()
        if target then
            Camera.CFrame = CFrame.new(Camera.CFrame.Position, target.Position)
        end
    end
end)

-- ==================== СКИНЧЕНДЖЕР ====================
local function applySkin(textureId)
    for _, item in pairs(Camera:GetDescendants()) do
        if item:IsA("MeshPart") or item:IsA("SpecialMesh") then
            item.TextureID = "rbxassetid://" .. tostring(textureId)
        end
    end
end

local BtnSkin1 = createButton("Скин: Золото", 135, Color3.fromRGB(200, 150, 0), MainFrame)
BtnSkin1.MouseButton1Click:Connect(function() applySkin(258021111) end)

local BtnSkin2 = createButton("Скин: Неон/Вулкан", 175, Color3.fromRGB(180, 50, 50), MainFrame)
BtnSkin2.MouseButton1Click:Connect(function() applySkin(286952864) end)

local BtnSkin3 = createButton("Скин: Азимов", 215, Color3.fromRGB(200, 100, 0), MainFrame)
BtnSkin3.MouseButton1Click:Connect(function() applySkin(311221431) end)

local BtnReset = createButton("Сбросить скин", 265, Color3.fromRGB(40, 40, 40), MainFrame)
BtnReset.MouseButton1Click:Connect(function() applySkin(0) end)
"""

SCRIPT_FILENAME = "xeno_menu.lua"
if not os.path.exists(SCRIPT_FILENAME):
    with open(SCRIPT_FILENAME, "w", encoding="utf-8") as f:
        f.write(LUA_CODE.strip())
    print(f"✅ Файл '{SCRIPT_FILENAME}' успешно создан!")

# ==========================================
# 3. КАТАЛОГ ТОВАРОВ И ПЕРЕВОДЫ
# ==========================================
SCRIPTS = {
    "xeno_menu": {
        "price": 15,  # Цена в Telegram Stars (⭐️)
        "file_name": SCRIPT_FILENAME,
        "title": {
            "ru": "Blox Strike: Xeno Menu",
            "ua": "Blox Strike: Xeno Menu",
            "en": "Blox Strike: Xeno Menu"
        },
        "description": {
            "ru": "Многофункциональное GUI-меню: ESP (ВХ), Плавный Аимбот на голову и Скинчейнджер (Золото, Вулкан, Азимов).",
            "ua": "Багатофункціональне GUI-меню: ESP (ВХ), Плавний Аімбот на голову та Скінчейнджер (Золото, Вулкан, Азімов).",
            "en": "Multifunctional GUI Menu: ESP (Wallhack), Smooth Head Aimbot, and Skinchanger (Gold, Vulcan, Asimov)."
        }
    }
}

TEXTS = {
    "ru": {
        "choose_lang": "🌐 Выберите язык / Оберіть мову / Choose language:",
        "start_msg": "👋 Добро пожаловать в Roblox Script Store!\n\nЗдесь можно купить проверенные Lua-скрипты за Telegram Stars (⭐️).\n\nВыберите нужный раздел в меню ниже:",
        "btn_catalog": "📁 Каталог скриптов",
        "btn_instruction": "ℹ️ Инструкция по установке",
        "btn_support": "👨‍💻 Поддержка",
        "btn_change_lang": "🌐 Сменить язык",
        "btn_back": "⬅️ Назад в меню",
        "catalog_title": "📁 Доступные скрипты:\n\nНажмите на скрипт, чтобы оформить заказ:",
        "instruction_text": "ℹ️ Как запустить купленный скрипт:\n\n1. Запустите ваш исполнитель скриптов (Delta, Hydrogen и т.д.) в Roblox.\n2. Скачайте полученный .lua файл или скопируйте его содержимое.\n3. Вставьте код в поле ввода инжектора/исполнителя.\n4. Нажмите Execute.",
        "support_text": f"👨‍💻 Служба поддержки\n\nПо всем вопросам и пополнению каталога обращайтесь:\n{SUPPORT_USERNAME}",
        "payment_success": "🎉 Оплата получена! ({amount} ⭐️)\n\nВаш файл {title} готов к скачиванию:"
    },
    "ua": {
        "choose_lang": "🌐 Выберите язык / Оберіть мову / Choose language:",
        "start_msg": "👋 Ласкаво просимо до Roblox Script Store!\n\nТут ви можете придбати перевірені Lua-скрипти за Telegram Stars (⭐️).\n\nОберіть потрібний розділ у меню нижче:",
        "btn_catalog": "📁 Каталог скриптів",
        "btn_instruction": "ℹ️ Інструкція з встановлення",
        "btn_support": "👨‍💻 Підтримка",
        "btn_change_lang": "🌐 Змінити мову",
        "btn_back": "⬅️ Назад до меню",
        "catalog_title": "📁 Доступні скрипти:\n\nНатисніть на скрипт, щоб оформити замовлення:",
        "instruction_text": "ℹ️ Як запустити придбаний скрипт:\n\n1. Запустіть ваш виконавець скриптів (Delta, Hydrogen тощо) у Roblox.\n2. Завантажте отриманий .lua файл або скопіюйте його вміст.\n3. Вставте код у поле введення інжектора/виконавця.\n4. Натисніть Execute.",
        "support_text": f"👨‍💻 Служба підтримки\n\nЗ усіх питань та з приводу поповнення каталогу звертайтеся:\n{SUPPORT_USERNAME}",
        "payment_success": "🎉 Оплату отримано! ({amount} ⭐️)\n\nВаш файл {title} готовий до завантаження:"
    },
    "en": {
        "choose_lang": "🌐 Choose language / Выберите язык / Оберіть мову:",
        "start_msg": "👋 Welcome to Roblox Script Store!\n\nHere you can buy verified Lua scripts for Telegram Stars (⭐️).\n\nChoose an option from the menu below:",
        "btn_catalog": "📁 Script Catalog",
        "btn_instruction": "ℹ️ Installation Guide",
        "btn_support": "👨‍💻 Support",
        "btn_change_lang": "🌐 Change language",
        "btn_back": "⬅️ Back to menu",
        "catalog_title": "📁 Available scripts:\n\nClick on a script to place an order:",
        "instruction_text": "ℹ️ How to run the purchased script:\n\n1. Launch your script executor (Delta, Hydrogen, etc.) in Roblox.\n2. Download the received .lua file or copy its content.\n3. Paste the code into the executor's input box.\n4. Click Execute.",
        "support_text": f"👨‍‍💻 Customer Support\n\nFor questions and catalog updates contact:\n{SUPPORT_USERNAME}",
        "payment_success": "🎉 Payment received! ({amount} ⭐️)\n\nYour file {title} is ready for download:"
    }
}

# Функция для получения языка пользователя (по умолчанию 'ru')
def get_user_lang(chat_id):
    return user_languages.get(chat_id, 'ru')

# ==========================================
# 4. МЕНЮ И КНОПКИ
# ==========================================
def language_selection_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")
    btn_ua = types.InlineKeyboardButton("🇺🇦 Українська", callback_data="set_lang_ua")
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")
    markup.add(btn_ru, btn_ua, btn_en)
    return markup

def main_menu_keyboard(lang):
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_catalog = types.InlineKeyboardButton(t["btn_catalog"], callback_data="menu_catalog")
    btn_instruction = types.InlineKeyboardButton(t["btn_instruction"], callback_data="menu_instruction")
    btn_support = types.InlineKeyboardButton(t["btn_support"], callback_data="menu_support")
    btn_lang = types.InlineKeyboardButton(t["btn_change_lang"], callback_data="menu_select_lang")
    markup.add(btn_catalog, btn_instruction, btn_support, btn_lang)
    return markup

def back_to_menu_keyboard(lang):
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="menu_main")
    markup.add(btn_back)
    return markup

# ==========================================
# 5. ОБРАБОТЧИКИ КОМАНД И НАВИГАЦИИ
# ==========================================
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        TEXTS["ru"]["choose_lang"],
        reply_markup=language_selection_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # --- Выбор языка ---
    if call.data.startswith("set_lang_"):
        lang = call.data.replace("set_lang_", "")
        user_languages[chat_id] = lang
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=TEXTS[lang]["start_msg"],
            reply_markup=main_menu_keyboard(lang)
        )

    elif call.data == "menu_select_lang":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=TEXTS[get_user_lang(chat_id)]["choose_lang"],
            reply_markup=language_selection_keyboard()
        )

    # --- Главное меню ---
    elif call.data == "menu_main":
        lang = get_user_lang(chat_id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=TEXTS[lang]["start_msg"],
            reply_markup=main_menu_keyboard(lang)
        )

    # --- Каталог скриптов ---
    elif call.data == "menu_catalog":
        lang = get_user_lang(chat_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for script_id, data in SCRIPTS.items():
            script_title = data["title"][lang]
            btn = types.InlineKeyboardButton(
                text=f"{script_title} — {data['price']} ⭐",
                callback_data=f"buy_{script_id}"
            )
            markup.add(btn)
        
        markup.add(types.InlineKeyboardButton(TEXTS[lang]["btn_back"], callback_data="menu_main"))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=TEXTS[lang]["catalog_title"],
            reply_markup=markup
        )

    # --- Инструкция ---
    elif call.data == "menu_instruction":
        lang = get_user_lang(chat_id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=TEXTS[lang]["instruction_text"],
            reply_markup=back_to_menu_keyboard(lang)
        )

    # --- Поддержка ---
    elif call.data == "menu_support":
        lang = get_user_lang(chat_id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=TEXTS[lang]["support_text"],
            reply_markup=back_to_menu_keyboard(lang)
        )

    # --- Оформление покупки за Звезды (⭐️) ---
    elif call.data.startswith("buy_"):
        script_id = call.data.replace("buy_", "")
        lang = get_user_lang(chat_id)
        
        if script_id in SCRIPTS:
            script_data = SCRIPTS[script_id]
            title = script_data['title'][lang]
            desc = script_data['description'][lang]

            bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=desc,
                invoice_payload=script_id,
                provider_token="",  # Для Telegram Stars поле оставляем пустым
                currency="XTR",    # Валюта Telegram Stars
                prices=[types.LabeledPrice(label=title, amount=script_data['price'])],
                start_parameter=f"buy-{script_id}"
            )
            bot.answer_callback_query(call.id)

# ==========================================
# 6. ОБРАБОТКА ОПЛАТЫ И ВЫДАЧА
# ==========================================
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    payment_info = message.successful_payment
    script_id = payment_info.invoice_payload
    lang = get_user_lang(message.chat.id)

    if script_id in SCRIPTS:
        script_data = SCRIPTS[script_id]
        title = script_data['title'][lang]
        success_msg = TEXTS[lang]["payment_success"].format(
            amount=payment_info.total_amount,
            title=title
        )

        bot.send_message(message.chat.id, success_msg)
        
        try:
            with open(script_data['file_name'], "rb") as file:
                bot.send_document(message.chat.id, file)
        except FileNotFoundError:
            bot.send_message(
                message.chat.id,
                f"⚠️ Error: File not found. Contact: {SUPPORT_USERNAME}"
            )

print("🚀 Мультиязычный бот маркетплейса запущен!")
bot.infinity_polling()
