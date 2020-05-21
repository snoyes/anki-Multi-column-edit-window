# Multi-column editor
![Multi-column editor](docs/multicolumn_browser.png)

## Rationale
If you're the kind of person who likes to have dozens and dozens of
field in your card type, this add-on is for you. In my personal use,
most field get very few content, such as a page number, a symbol,
etc... Those fields does not need to take the full width of the
window. This add-on simply allow you to have multiple field on a
single line.

Of course, some fields may contain a lot of text. In this case you may
want to take the full window width. This add-on also permit it. You
will have small fields and big fields.

## Frozen Field

Current version of the add-on "Frozen Field" is not compatible with
this add-on. Please use add-on
[389392894](https://ankiweb.net/shared/info/389392894) instead.

## Configuration
On the bottom right of the editor/add card/browser, you will see a
number. Changing this number change the number of columns.

Near field names, you will see either `&raquo;-&laquo;` or
`&laquo;-&raquo;`. Those two buttons allows to switch the field
between short and big size. I.e. decide whether the field shares its
line or take the line alone.

A shortcut (by default F10) allow to switch the currently select
field's size.

## Internal
The configuration is saved in anki's note type, so that when you
synchronize your collection, you'll have the same number of column
when you change your computer.

It redefines the editor.js's method `setField`

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | HSSM (2013-2018)
and         | Arthur Milchior <arthur@milchior.fr> (2018-2020)
and         | rarer external contributions
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU GPL, version 3 or later; http://www.gnu.org/licenses/gpl.html
Source in   | https://github.com/Arthur-Milchior/anki-Multi-column-edit-window
Addon number| [3491767031](https://ankiweb.net/shared/info/3491767031)
