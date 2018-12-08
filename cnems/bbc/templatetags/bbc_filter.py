from django import template
register = template.Library()

@register.filter(name='check_status')
def check_status(n):

    if n.news_check == '0':
        src = '/static/bbc/img/dsh.png'
        return src
    elif n.news_check == '-1':
        src = '/static/bbc/img/wtg.png'
        return src
    else:
        src = ''
        return src




from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page, loop_page):
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<li class="activate"><a href="?page=%s">%s</a></li>'%(loop_page, loop_page)
        else:
            page_ele = '<li><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)

        return format_html(page_ele)
    else:
        return ''

@register.filter()
def change_str(value):
    if len(value) > 20:
        return value[:40]+'......'
    return value

