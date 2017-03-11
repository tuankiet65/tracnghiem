pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot -k i18n.translate .
pybabel update -i translations/messages.pot -d translations
