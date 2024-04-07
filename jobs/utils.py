from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Job, Contract
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def generate_contract_pdf(request, contract_id):
    # Retrieve the Job and Contract data from your models
    # job = Job.objects.get(pk=job_id)
    contract = Contract.objects.get(id=contract_id)
    job = contract.job


    # Create a response object with appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contract_{job.id}.pdf"'

    # Create the PDF content using ReportLab
    p = canvas.Canvas(response, pagesize=letter)

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 770, 'Yollanma.uz Vazifa Bajarish Shartnomasi')

    # Contract Details
    p.setFont("Helvetica", 12)
    y_position = 750

    # Task Details
    p.drawString(50, y_position, 'Shartnoma Tafsilotlari:')
    y_position -= 15
    p.drawString(50, y_position, f'1. Vazifa IDsi: {job.id}')
    y_position -= 15
    p.drawString(50, y_position, f'2. Vazifa nomi: {job.title}')
    y_position -= 15
    p.drawString(50, y_position, f'3. Vazifa Tasnifi: {job.description}')
    y_position -= 25

    # Parties
    p.drawString(50, y_position, 'Taraflar:')
    y_position -= 15
    p.drawString(70, y_position, 'Buyurtmachi:')
    y_position -= 15
    p.drawString(90, y_position, f'  - Foydalanuvchi nomi: {contract.client.username}')
    y_position -= 15
    p.drawString(90, y_position, f'  - Ism: {contract.client.name}')
    y_position -= 15
    p.drawString(70, y_position, 'Frilanser:')
    y_position -= 15
    p.drawString(90, y_position, f'  - Foydalanuvchi nomi: {contract.freelancer.username}')
    y_position -= 15
    p.drawString(90, y_position, f'  - Ism: {contract.freelancer.name}')
    y_position -= 25

    p.drawString(50, y_position, 'Shartnoma :')
    y_position -= 15
    p.drawString(70, y_position, f'3. Narx: Vazifa uchun kelgan narx {job.budget} O\'zbek so\'mi bo\'lganiga rozilik bildirilgan.')
    y_position -= 15
    p.drawString(70, y_position, f'4. Davr: Vazifani bajarish muddati {job.duration} kun bo\'lganiga rozilik bildirilgan.')
    y_position -= 25

    # Shartnoma Shartlari
    p.drawString(50, y_position, 'Shartnoma Shartlari:')
    y_position -= 15
    p.drawString(70, y_position, '5. Ishning miqyosi:')
    y_position -= 15
    p.drawString(90, y_position, f'  - Frilans vazifani vazifa tafsilotlarida ta\'riflanganicha bajarishga rozilik bildiradi.')
    y_position -= 15
    p.drawString(70, y_position, '6. To\'lov va Hisob-kitob:')
    y_position -= 15
    p.drawString(90, y_position, f'  - To\'lov tafsilotlari va hisob-kitob shartlari Mijoz va Frilans o\'rtasida mustaqil ravishda muvofiqlashtirilgan.')
    y_position -= 15
    p.drawString(70, y_position, '7. Muloqot:')
    y_position -= 15
    p.drawString(90, y_position, f'  - Vazifa bo\'yicha muhim muloqotlar hujjatlar saqlash maqsadida Frilans Bazar xabarlash tizimida bo\'lishi kerak.')
    y_position -= 15
    p.drawString(90, y_position, f'  - Vazifa bilan bog\'liq vazifani, rivojlanish yangilanishlarini va oxirgi fayllarni faqatgina platformaning ichki muloqot kanalida almashish va hujjatlash kerak.')
    y_position -= 15
    p.drawString(90, y_position, f'  - Tashqi muloqotlar boshqa xabarlovchilar orqali amalga oshirilsa ham, bu ish yoki muloqotni isbotlash uchun xizmat qilmaydi.')
    y_position -= 25

    # Taqiqlangan Kontent
    p.drawString(50, y_position, 'Taqiqlangan Kontent:')
    y_position -= 15
    p.drawString(70, y_position, '8. Taqiqlangan Kontent:')
    y_position -= 15
    p.drawString(90, y_position, '  - Both parties acknowledge that it is strictly prohibited to include content in the task that involves or promotes pornography, violence, hate speech, discrimination, illegal activities, politically biased content, or any material that violates the laws and regulations of the Republic of Uzbekistan or any relevant jurisdiction.')
    y_position -= 25

    # Hukumat Qonuni
    p.drawString(50, y_position, 'Hukumat Qonuni:')
    y_position -= 15
    p.drawString(70, y_position, '9. Hukumat Qonuni:')
    y_position -= 15
    p.drawString(90, y_position, '  - Ushbu Shartnoma O\'zbekiston Respublikasining qonunlariga muvofiq qayd etilgan va shariyat etilgan.')
    y_position -= 25

    # Aloqa Ma'lumotlari
    p.drawString(50, y_position, 'Aloqa Ma\'lumotlari:')
    y_position -= 15
    p.drawString(70, y_position, '10. Aloqa:')
    y_position -= 15
    p.drawString(90, y_position, f'  - Ushbu Shartnomaga oid so\'rovnoma yoki muammoatlaringiz bo\'yicha aaaa@aaa.com ga murojaat qiling.')
    y_position -= 25

    # Shartnoma
    y_position -= 15
    p.drawString(50, y_position, 'Shartnoma:')
    y_position -= 15
    p.drawString(70, y_position, 'Ushbu vazifani qabul qilish va shartnoma qilish orqali, ikkala tomonda ushbu Vazifa Shartnomasida belgilangan shartlarni o\'qiganligini, tushunishini va unga rioya etishini tasdiqlashadi. Agar ushbu shartlarning istalgan qismiga muammo bo\'lsa, tomonlar tezroq muloqot qilishi kerak.')
    y_position -= 25

    # Platform Ma'lumotlari
    p.drawString(50, y_position, 'Frilans Bazar')
    y_position -= 15
    p.drawString(70, y_position, '[Manzil]')
    y_position -= 15
    p.drawString(70, y_position, '[Sana]')
    y_position -= 25

    # # Signatures
    # y_position -= 15
    # p.drawString(50, y_position, 'Client\'s Signature: Signed')
    # y_position -= 15
    # p.drawString(50, y_position, 'Freelancer\'s Signature: _______________________')

    # Save the PDF content
    p.showPage()
    p.save()

    return response


def searchJobs(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    jobObj = Job.objects.distinct().filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    return jobObj, search_query


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    # results = 3
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, profiles
