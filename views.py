import logging
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .models import Fbpage
from .models import Fbdate
from .forms import InquiryForm
from .searchforms import SearchForm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:index')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class SearchView(generic.CreateView, generic.FormView):
    template_name = "search.html"
    form_class = SearchForm
    model = Fbpage
    success_url = reverse_lazy('diary:fbpage_list')

    def post(self, request, *args, **kwargs):
        d = request.POST['id_number']
        options = Options()
        options.add_argument('--headless')
        # ブラウザを起動する
        driver = webdriver.Chrome(chrome_options=options)
        # ブラウザでアクセスする

        driver.get(
            "https://ja-jp.facebook.com/ads/library/?active_status=all&ad_type=all&country=JP&impression_search_field=has_impressions_lifetime&view_all_page_id={h}".format(
                h=d))

        driver.implicitly_wait(10)

        height = driver.execute_script("return document.body.scrollHeight")

        # ループ処理で少しづつ移動
        for x in range(1, height):
            driver.execute_script("window.scrollTo(0, " + str(50 * x) + ");")

        name = driver.find_element_by_css_selector('._8wh_').text
        date1 = driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]').text
        date2 = driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[1]').text

        f = Fbpage(facebook_page=name, id_number=d, category_name=date1, good_number=date2)
        f.save()

        if len(driver.find_elements_by_css_selector('._7gn2')) > 0:
            t = driver.find_elements_by_css_selector(('._7owt'))
            for s in t:
                if len(s.find_elements_by_css_selector('._7jys')) > 0:
                    image = s.find_element_by_css_selector('._7jys').get_attribute('src')
                    text = s.find_element_by_css_selector('._7jyr').text
                    k_id = s.find_element_by_css_selector('._4rhp').text
                    day = s.find_element_by_css_selector('._7jwu').text
                    h = Fbdate(photo=image, id_number=d, text=text, k_id=k_id, day=day)
                    h.save()
            else:
                print('なし')

        else:
            print('なし')


        driver.quit()
        return redirect('diary:fbpage_list')


class FbpageView(generic.ListView):
    model = Fbpage
    template_name = 'fbpage_list.html'


    def list(self):
        fbpages = Fbpage.objects.all()
        return fbpages


def FbimageView(request):
    d = {
        "fbdates": Fbdate.objects.all()
       }
    return render(request, 'fbpage_image.html', d)

class FbpageDetailView(generic.DetailView):
    model = Fbpage
    template_name = "fbpage_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['d'] = Fbpage.objects.get(pk=self.kwargs.get('pk'))
        id = Fbpage.objects.values('id_number').get(pk=self.kwargs.get('pk'))
        context['date'] = Fbdate.objects.filter(id_number=id["id_number"])
        return context