//! moment.js locale configuration
//! locale : Russian [ru]
//! author : Viktorminator : https://github.com/Viktorminator
//! Author : Menelion ElensГєle : https://github.com/Oire
//! author : РљРѕСЂРµРЅР±РµСЂРі РњР°СЂРє : https://github.com/socketpair

;(function (global, factory) {
   typeof exports === 'object' && typeof module !== 'undefined'
       && typeof require === 'function' ? factory(require('../moment')) :
   typeof define === 'function' && define.amd ? define(['../moment'], factory) :
   factory(global.moment)
}(this, function (moment) { 'use strict';


    function plural(word, num) {
        var forms = word.split('_');
        return num % 10 === 1 && num % 100 !== 11 ? forms[0] : (num % 10 >= 2 && num % 10 <= 4 && (num % 100 < 10 || num % 100 >= 20) ? forms[1] : forms[2]);
    }
    function relativeTimeWithPlural(number, withoutSuffix, key) {
        var format = {
            'mm': withoutSuffix ? 'РјРёРЅСѓС‚Р°_РјРёРЅСѓС‚С‹_РјРёРЅСѓС‚' : 'РјРёРЅСѓС‚Сѓ_РјРёРЅСѓС‚С‹_РјРёРЅСѓС‚',
            'hh': 'С‡Р°СЃ_С‡Р°СЃР°_С‡Р°СЃРѕРІ',
            'dd': 'РґРµРЅСЊ_РґРЅСЏ_РґРЅРµР№',
            'MM': 'РјРµСЃСЏС†_РјРµСЃСЏС†Р°_РјРµСЃСЏС†РµРІ',
            'yy': 'РіРѕРґ_РіРѕРґР°_Р»РµС‚'
        };
        if (key === 'm') {
            return withoutSuffix ? 'РјРёРЅСѓС‚Р°' : 'РјРёРЅСѓС‚Сѓ';
        }
        else {
            return number + ' ' + plural(format[key], +number);
        }
    }
    var monthsParse = [/^СЏРЅРІ/i, /^С„РµРІ/i, /^РјР°СЂ/i, /^Р°РїСЂ/i, /^РјР°[Р№СЏ]/i, /^РёСЋРЅ/i, /^РёСЋР»/i, /^Р°РІРі/i, /^СЃРµРЅ/i, /^РѕРєС‚/i, /^РЅРѕСЏ/i, /^РґРµРє/i];

    // http://new.gramota.ru/spravka/rules/139-prop : В§ 103
    // РЎРѕРєСЂР°С‰РµРЅРёСЏ РјРµСЃСЏС†РµРІ: http://new.gramota.ru/spravka/buro/search-answer?s=242637
    // CLDR data:          http://www.unicode.org/cldr/charts/28/summary/ru.html#1753
    var ru = moment.defineLocale('ru', {
        months : {
            format: 'СЏРЅРІР°СЂСЏ_С„РµРІСЂР°Р»СЏ_РјР°СЂС‚Р°_Р°РїСЂРµР»СЏ_РјР°СЏ_РёСЋРЅСЏ_РёСЋР»СЏ_Р°РІРіСѓСЃС‚Р°_СЃРµРЅС‚СЏР±СЂСЏ_РѕРєС‚СЏР±СЂСЏ_РЅРѕСЏР±СЂСЏ_РґРµРєР°Р±СЂСЏ'.split('_'),
            standalone: 'СЏРЅРІР°СЂСЊ_С„РµРІСЂР°Р»СЊ_РјР°СЂС‚_Р°РїСЂРµР»СЊ_РјР°Р№_РёСЋРЅСЊ_РёСЋР»СЊ_Р°РІРіСѓСЃС‚_СЃРµРЅС‚СЏР±СЂСЊ_РѕРєС‚СЏР±СЂСЊ_РЅРѕСЏР±СЂСЊ_РґРµРєР°Р±СЂСЊ'.split('_')
        },
        monthsShort : {
            // РїРѕ CLDR РёРјРµРЅРЅРѕ "РёСЋР»." Рё "РёСЋРЅ.", РЅРѕ РєР°РєРѕР№ СЃРјС‹СЃР» РјРµРЅСЏС‚СЊ Р±СѓРєРІСѓ РЅР° С‚РѕС‡РєСѓ ?
            format: 'СЏРЅРІ._С„РµРІСЂ._РјР°СЂ._Р°РїСЂ._РјР°СЏ_РёСЋРЅСЏ_РёСЋР»СЏ_Р°РІРі._СЃРµРЅС‚._РѕРєС‚._РЅРѕСЏР±._РґРµРє.'.split('_'),
            standalone: 'СЏРЅРІ._С„РµРІСЂ._РјР°СЂС‚_Р°РїСЂ._РјР°Р№_РёСЋРЅСЊ_РёСЋР»СЊ_Р°РІРі._СЃРµРЅС‚._РѕРєС‚._РЅРѕСЏР±._РґРµРє.'.split('_')
        },
        weekdays : {
            standalone: 'РІРѕСЃРєСЂРµСЃРµРЅСЊРµ_РїРѕРЅРµРґРµР»СЊРЅРёРє_РІС‚РѕСЂРЅРёРє_СЃСЂРµРґР°_С‡РµС‚РІРµСЂРі_РїСЏС‚РЅРёС†Р°_СЃСѓР±Р±РѕС‚Р°'.split('_'),
            format: 'РІРѕСЃРєСЂРµСЃРµРЅСЊРµ_РїРѕРЅРµРґРµР»СЊРЅРёРє_РІС‚РѕСЂРЅРёРє_СЃСЂРµРґСѓ_С‡РµС‚РІРµСЂРі_РїСЏС‚РЅРёС†Сѓ_СЃСѓР±Р±РѕС‚Сѓ'.split('_'),
            isFormat: /\[ ?[Р’РІ] ?(?:РїСЂРѕС€Р»СѓСЋ|СЃР»РµРґСѓСЋС‰СѓСЋ|СЌС‚Сѓ)? ?\] ?dddd/
        },
        weekdaysShort : 'РІСЃ_РїРЅ_РІС‚_СЃСЂ_С‡С‚_РїС‚_СЃР±'.split('_'),
        weekdaysMin : 'РІСЃ_РїРЅ_РІС‚_СЃСЂ_С‡С‚_РїС‚_СЃР±'.split('_'),
        monthsParse : monthsParse,
        longMonthsParse : monthsParse,
        shortMonthsParse : monthsParse,

        // РїРѕР»РЅС‹Рµ РЅР°Р·РІР°РЅРёСЏ СЃ РїР°РґРµР¶Р°РјРё, РїРѕ С‚СЂРё Р±СѓРєРІС‹, РґР»СЏ РЅРµРєРѕС‚РѕСЂС‹С…, РїРѕ 4 Р±СѓРєРІС‹, СЃРѕРєСЂР°С‰РµРЅРёСЏ СЃ С‚РѕС‡РєРѕР№ Рё Р±РµР· С‚РѕС‡РєРё
        monthsRegex: /^(СЏРЅРІР°СЂ[СЊСЏ]|СЏРЅРІ\.?|С„РµРІСЂР°Р»[СЊСЏ]|С„РµРІСЂ?\.?|РјР°СЂС‚Р°?|РјР°СЂ\.?|Р°РїСЂРµР»[СЊСЏ]|Р°РїСЂ\.?|РјР°[Р№СЏ]|РёСЋРЅ[СЊСЏ]|РёСЋРЅ\.?|РёСЋР»[СЊСЏ]|РёСЋР»\.?|Р°РІРіСѓСЃС‚Р°?|Р°РІРі\.?|СЃРµРЅС‚СЏР±СЂ[СЊСЏ]|СЃРµРЅС‚?\.?|РѕРєС‚СЏР±СЂ[СЊСЏ]|РѕРєС‚\.?|РЅРѕСЏР±СЂ[СЊСЏ]|РЅРѕСЏР±?\.?|РґРµРєР°Р±СЂ[СЊСЏ]|РґРµРє\.?)/i,

        // РєРѕРїРёСЏ РїСЂРµРґС‹РґСѓС‰РµРіРѕ
        monthsShortRegex: /^(СЏРЅРІР°СЂ[СЊСЏ]|СЏРЅРІ\.?|С„РµРІСЂР°Р»[СЊСЏ]|С„РµРІСЂ?\.?|РјР°СЂС‚Р°?|РјР°СЂ\.?|Р°РїСЂРµР»[СЊСЏ]|Р°РїСЂ\.?|РјР°[Р№СЏ]|РёСЋРЅ[СЊСЏ]|РёСЋРЅ\.?|РёСЋР»[СЊСЏ]|РёСЋР»\.?|Р°РІРіСѓСЃС‚Р°?|Р°РІРі\.?|СЃРµРЅС‚СЏР±СЂ[СЊСЏ]|СЃРµРЅС‚?\.?|РѕРєС‚СЏР±СЂ[СЊСЏ]|РѕРєС‚\.?|РЅРѕСЏР±СЂ[СЊСЏ]|РЅРѕСЏР±?\.?|РґРµРєР°Р±СЂ[СЊСЏ]|РґРµРє\.?)/i,

        // РїРѕР»РЅС‹Рµ РЅР°Р·РІР°РЅРёСЏ СЃ РїР°РґРµР¶Р°РјРё
        monthsStrictRegex: /^(СЏРЅРІР°СЂ[СЏСЊ]|С„РµРІСЂР°Р»[СЏСЊ]|РјР°СЂС‚Р°?|Р°РїСЂРµР»[СЏСЊ]|РјР°[СЏР№]|РёСЋРЅ[СЏСЊ]|РёСЋР»[СЏСЊ]|Р°РІРіСѓСЃС‚Р°?|СЃРµРЅС‚СЏР±СЂ[СЏСЊ]|РѕРєС‚СЏР±СЂ[СЏСЊ]|РЅРѕСЏР±СЂ[СЏСЊ]|РґРµРєР°Р±СЂ[СЏСЊ])/i,

        // Р’С‹СЂР°Р¶РµРЅРёРµ, РєРѕС‚РѕСЂРѕРµ СЃРѕРѕС‚РІРµСЃС‚РІСѓРµС‚ С‚РѕР»СЊРєРѕ СЃРѕРєСЂР°С‰С‘РЅРЅС‹Рј С„РѕСЂРјР°Рј
        monthsShortStrictRegex: /^(СЏРЅРІ\.|С„РµРІСЂ?\.|РјР°СЂ[С‚.]|Р°РїСЂ\.|РјР°[СЏР№]|РёСЋРЅ[СЊСЏ.]|РёСЋР»[СЊСЏ.]|Р°РІРі\.|СЃРµРЅС‚?\.|РѕРєС‚\.|РЅРѕСЏР±?\.|РґРµРє\.)/i,
        longDateFormat : {
            LT : 'HH:mm',
            LTS : 'HH:mm:ss',
            L : 'DD.MM.YYYY',
            LL : 'D MMMM YYYY Рі.',
            LLL : 'D MMMM YYYY Рі., HH:mm',
            LLLL : 'dddd, D MMMM YYYY Рі., HH:mm'
        },
        calendar : {
            sameDay: '[РЎРµРіРѕРґРЅСЏ РІ] LT',
            nextDay: '[Р—Р°РІС‚СЂР° РІ] LT',
            lastDay: '[Р’С‡РµСЂР° РІ] LT',
            nextWeek: function (now) {
                if (now.week() !== this.week()) {
                    switch (this.day()) {
                        case 0:
                            return '[Р’ СЃР»РµРґСѓСЋС‰РµРµ] dddd [РІ] LT';
                        case 1:
                        case 2:
                        case 4:
                            return '[Р’ СЃР»РµРґСѓСЋС‰РёР№] dddd [РІ] LT';
                        case 3:
                        case 5:
                        case 6:
                            return '[Р’ СЃР»РµРґСѓСЋС‰СѓСЋ] dddd [РІ] LT';
                    }
                } else {
                    if (this.day() === 2) {
                        return '[Р’Рѕ] dddd [РІ] LT';
                    } else {
                        return '[Р’] dddd [РІ] LT';
                    }
                }
            },
            lastWeek: function (now) {
                if (now.week() !== this.week()) {
                    switch (this.day()) {
                        case 0:
                            return '[Р’ РїСЂРѕС€Р»РѕРµ] dddd [РІ] LT';
                        case 1:
                        case 2:
                        case 4:
                            return '[Р’ РїСЂРѕС€Р»С‹Р№] dddd [РІ] LT';
                        case 3:
                        case 5:
                        case 6:
                            return '[Р’ РїСЂРѕС€Р»СѓСЋ] dddd [РІ] LT';
                    }
                } else {
                    if (this.day() === 2) {
                        return '[Р’Рѕ] dddd [РІ] LT';
                    } else {
                        return '[Р’] dddd [РІ] LT';
                    }
                }
            },
            sameElse: 'L'
        },
        relativeTime : {
            future : 'С‡РµСЂРµР· %s',
            past : '%s РЅР°Р·Р°Рґ',
            s : 'РЅРµСЃРєРѕР»СЊРєРѕ СЃРµРєСѓРЅРґ',
            m : relativeTimeWithPlural,
            mm : relativeTimeWithPlural,
            h : 'С‡Р°СЃ',
            hh : relativeTimeWithPlural,
            d : 'РґРµРЅСЊ',
            dd : relativeTimeWithPlural,
            M : 'РјРµСЃСЏС†',
            MM : relativeTimeWithPlural,
            y : 'РіРѕРґ',
            yy : relativeTimeWithPlural
        },
        meridiemParse: /РЅРѕС‡Рё|СѓС‚СЂР°|РґРЅСЏ|РІРµС‡РµСЂР°/i,
        isPM : function (input) {
            return /^(РґРЅСЏ|РІРµС‡РµСЂР°)$/.test(input);
        },
        meridiem : function (hour, minute, isLower) {
            if (hour < 4) {
                return 'РЅРѕС‡Рё';
            } else if (hour < 12) {
                return 'СѓС‚СЂР°';
            } else if (hour < 17) {
                return 'РґРЅСЏ';
            } else {
                return 'РІРµС‡РµСЂР°';
            }
        },
        ordinalParse: /\d{1,2}-(Р№|РіРѕ|СЏ)/,
        ordinal: function (number, period) {
            switch (period) {
                case 'M':
                case 'd':
                case 'DDD':
                    return number + '-Р№';
                case 'D':
                    return number + '-РіРѕ';
                case 'w':
                case 'W':
                    return number + '-СЏ';
                default:
                    return number;
            }
        },
        week : {
            dow : 1, // Monday is the first day of the week.
            doy : 7  // The week that contains Jan 1st is the first week of the year.
        }
    });

    return ru;

}));