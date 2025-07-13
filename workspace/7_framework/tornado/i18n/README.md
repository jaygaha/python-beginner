# Tornado Internationalization (i18n) Implementation

A comprehensive example of implementing internationalization and localization in Tornado web applications, demonstrating multi-language support with dynamic locale switching.

## Overview

This implementation showcases Tornado's built-in internationalization capabilities, featuring:

- **Multi-language Support** - English (US) and Japanese translations
- **Dynamic Locale Detection** - URL-based locale routing
- **Template Localization** - Translated content rendering
- **Language Switching** - User-friendly locale switching interface
- **CSV Translation Files** - Simple translation management
- **Parameterized Translations** - Dynamic content with placeholders

## Project Structure

```
i18n/
├── app.py                 # Main application with i18n handlers
├── README.md             # This documentation
├── locale/               # Translation files directory
│   ├── en_US.csv        # English translations
│   └── ja_JP.csv        # Japanese translations
└── templates/           # Localized templates
    └── index.html       # Multi-language template
```

## Features

### Supported Languages

- **English (US)** - `en_US` locale
- **Japanese** - `ja_JP` locale

### Core Functionality

- **URL-based Locale Routing** - `/en_US/about-us` and `/ja_JP/about-us`
- **Automatic Locale Detection** - Falls back to English for unsupported locales
- **Template Translation** - Uses `{{ _("key") }}` syntax for translations
- **Parameter Substitution** - Dynamic content with `%(variable)s` placeholders
- **Language Switching UI** - Flag-based locale switcher with emoji flags

## Installation

1. Ensure you have Tornado installed:
```bash
pip install tornado
```

2. Run the application:
```bash
python app.py
```

3. Access the application:
   - English: `http://localhost:8880/en_US/about-us`
   - Japanese: `http://localhost:8880/ja_JP/about-us`

## Usage

### Basic Setup

The application automatically loads translation files on startup:

```python
tornado.locale.load_translations("locale/")
```

### URL Routing

URLs follow the pattern `/{locale}/about-us` where locale is either `en_US` or `ja_JP`:

```python
(r"/(?P<locale>[a-z]{2}_[A-Z]{2})/about-us", LocaleHandler),
```

### Locale Handling

The `BaseHandler` provides locale detection:

```python
class BaseHandler(tornado.web.RequestHandler):
    def get_user_locale(self):
        locale_code = self.path_kwargs.get("locale", "en_US")
        return tornado.locale.get(locale_code)
```

## Translation Files

### CSV Format

Translations are stored in CSV files with the format: `key,translation`

#### English (`locale/en_US.csv`)
```csv
home,Home
plans,Plans
about,About
contact,Contact
what-we-offer,What We Offer
design,Design
branding,Branding
consultation,Consultation
promises,Promises
footer,Footer
top,To the top
design-description,Modern and realistic designs
branding-description,An effective brand strategy gives you a major edge in increasingly competitive markets
consultation-description,Free consultation services and 24/7 on-call support
promises-description,High-quality product to customers,singular
promises-description,High-quality products to customers,plural
created-by,Created by %(author)s
total-view,%(view)d total views
```

#### Japanese (`locale/ja_JP.csv`)
```csv
home,ホーム
plans,プラン
about,について
contact,コンタクト
what-we-offer,サービス内容
design,デザイン
branding,ブランディング
consultation,相談
promises,約束
footer,フッター
top,トップ
design-description,モダンでリアルなデザイン
branding-description,効果的なブランド戦略は、競争が激化する市場で大きな優位性をもたらします。
consultation-description,無料の相談サービスと24時間365日のオンコールサポート
promises-description,お客様に高品質な製品をお届け,singular
promises-description,お客様に高品質な製品をお届け,plural
created-by,%(author)s によって作成されました
total-view,合計閲覧回数 %(view)d
```

### Translation Features

#### Simple Translations
```python
# Template usage
{{ _("home") }}  # Returns "Home" or "ホーム"
```

#### Parameterized Translations
```python
# Template usage with parameters
{{ _("created-by") % {"author": author} }}
# Returns "Created by Jay" or "Jay によって作成されました"
```

#### Plural Forms
```python
# CSV supports singular/plural forms
promises-description,High-quality product to customers,singular
promises-description,High-quality products to customers,plural
```

## Template Integration

### Translation Syntax

Templates use Tornado's `{{ _("key") }}` syntax for translations:

```html
<nav>
    <a href="#">{{ _("home") }}</a>
    <a href="#">{{ _("plans") }}</a>
    <a href="#">{{ _("about") }}</a>
    <a href="#">{{ _("contact") }}</a>
</nav>
```

### Language Switcher

The template includes a language switcher with emoji flags:

```html
<div class="lang-switcher">
    <a href="/{{ switch_locale }}/about-us" title="{{ lang_name }}">{{ flag }}</a>
</div>
```

### Dynamic Content

Templates can include dynamic content with parameter substitution:

```html
<p>{{ _("created-by") % {"author": author} }}</p>
<p>{{ _("total-view") % {"view": view} }}</p>
```

## Handler Implementation

### Locale Handler

The main handler manages locale detection and template rendering:

```python
class LocaleHandler(BaseHandler):
    def get(self, locale):
        # Normalize and set locale
        locale = locale if locale in ("en_US", "ja_JP") else "en_US"
        self.locale = tornado.locale.get(locale)

        # Determine language switching
        if locale == "en_US":
            switch_locale = "ja_JP"
            flag = "🇯🇵"
            lang_name = "日本語"
        else:
            switch_locale = "en_US"
            flag = "🇺🇸"
            lang_name = "English"

        self.render("index.html",
                    current_locale=locale,
                    switch_locale=switch_locale,
                    lang_name=lang_name,
                    flag=flag,
                    product="Pro Suite",
                    author="Jay",
                    view=8880)
```

## Adding New Languages

### 1. Create Translation File

Add a new CSV file in the `locale/` directory:

```csv
# locale/es_ES.csv
home,Inicio
plans,Planes
about,Acerca de
contact,Contacto
# ... more translations
```

### 2. Update Handler Logic

Modify the `LocaleHandler` to support the new locale:

```python
def get(self, locale):
    # Add new locale to supported list
    locale = locale if locale in ("en_US", "ja_JP", "es_ES") else "en_US"
    
    # Add language switching logic
    if locale == "es_ES":
        switch_locale = "en_US"
        flag = "🇪🇸"
        lang_name = "Español"
    # ... existing logic
```

### 3. Update URL Pattern

The existing URL pattern already supports the new locale format:

```python
(r"/(?P<locale>[a-z]{2}_[A-Z]{2})/about-us", LocaleHandler),
```

## Best Practices

### Translation Management

1. **Consistent Keys** - Use descriptive, consistent translation keys
2. **Parameterization** - Use `%(variable)s` for dynamic content
3. **Plural Forms** - Support singular/plural forms where needed
4. **Context** - Include context in key names (e.g., `button-save`, `title-welcome`)

### Code Organization

1. **Base Handler** - Centralize locale detection logic
2. **Fallback Locale** - Always provide a default locale
3. **Validation** - Validate locale parameters to prevent errors
4. **Caching** - Consider caching translations for performance

### Template Design

1. **Responsive Design** - Account for different text lengths across languages
2. **RTL Support** - Consider right-to-left languages if needed
3. **Font Support** - Ensure fonts support all character sets
4. **Cultural Considerations** - Adapt UI elements for different cultures

## Performance Considerations

### Loading Translations

- **Startup Loading** - Translations are loaded once at application startup
- **Memory Usage** - All translations are kept in memory for fast access
- **File Format** - CSV format is simple and efficient for small translation sets

### Optimization Tips

1. **Lazy Loading** - Load translations only when needed for large applications
2. **Caching** - Cache rendered templates with translations
3. **CDN** - Use CDN for static assets across different locales
4. **Compression** - Enable gzip compression for translated content

## Testing

### Manual Testing

Test different locales by accessing:

```bash
# English
curl http://localhost:8880/en_US/about-us

# Japanese
curl http://localhost:8880/ja_JP/about-us

# Unsupported locale (falls back to English)
curl http://localhost:8880/fr_FR/about-us
```

### Browser Testing

1. Open `http://localhost:8880/en_US/about-us` in your browser
2. Click the Japanese flag (🇯🇵) to switch to Japanese
3. Click the American flag (🇺🇸) to switch back to English
4. Verify all text elements are properly translated

## Common Issues and Solutions

### Missing Translations

**Problem**: Translation key not found
**Solution**: Check CSV file format and ensure key exists in all language files

### Encoding Issues

**Problem**: Special characters not displaying correctly
**Solution**: Ensure CSV files are saved with UTF-8 encoding

### Template Errors

**Problem**: Template rendering fails
**Solution**: Verify template syntax and ensure all variables are passed to render()

### Locale Detection

**Problem**: Wrong locale being detected
**Solution**: Check URL pattern and locale validation logic

## Extending the Implementation

### Database-backed Translations

For larger applications, consider storing translations in a database:

```python
class DatabaseLocale(tornado.locale.Locale):
    def __init__(self, code):
        super().__init__(code)
        self.load_from_database()
    
    def load_from_database(self):
        # Load translations from database
        pass
```

### Dynamic Translation Updates

Implement admin interface for managing translations:

```python
class TranslationHandler(tornado.web.RequestHandler):
    async def post(self):
        # Update translation in database
        # Reload locale cache
        pass
```

### Pluralization Rules

Implement complex pluralization rules:

```python
def pluralize(self, key, count):
    # Implement language-specific pluralization
    if self.code == "en_US":
        return key + "s" if count != 1 else key
    # ... other languages
```

## Resources

- **Tornado Locale Documentation** - https://tornadoweb.org/en/stable/locale.html
- **Unicode CLDR** - Common Locale Data Repository
- **ISO 639 Language Codes** - Standard language identifiers
- **ISO 3166 Country Codes** - Standard country identifiers

## License

This implementation is provided as educational material demonstrating Tornado's internationalization capabilities.