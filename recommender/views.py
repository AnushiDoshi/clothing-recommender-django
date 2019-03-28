from django.shortcuts import render, get_object_or_404, redirect
from recommender.models import Item, Preferences
from django.views import generic
from django.views.generic import RedirectView
from django.db.models import Max, Count
from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
import re
from collections import defaultdict
from django.urls import reverse
import traceback


file = open('test.txt', 'a')



def index(request):
	random_items = Item.objects.order_by('?').only('image_URL')[:21]
	context = {

		'random_items': random_items,
	}
	return render(request, 'index.html', context)
def RecommendedListView(request):
	model = Item
	template_name = 'recommender/recommended.html'
	paginate_by = 10
	
	def get_sim(pref, liked_index_list, user_preference_list):
		pk_list = []
		pks = []
		top_val_1 = []
		desc_coe_list = []
		random_items = []
		dice_coe = defaultdict(int)
		upl = user_preference_list.copy()
		print(upl)
		#print(pref)
		column_mapping = {'item_type': 0, 'color': 1, 'fit': 2, 'occasion': 3, 'brand': 4, 'pattern': 5, 'fabric':6, 'length': 7}
		lastkey = Item.objects.only('id').order_by('-id').first()
		print(lastkey.id)
		firstkey = Item.objects.only('id').order_by('id').first()
		print(firstkey.id)
		for pk in Item.objects.only('id').values('id'):
			if pk['id'] in liked_index_list:
				continue
			else:
				pks.append(pk['id'])

		#print(len(pks))
		for i in range(int(firstkey.id), int(lastkey.id)):
			if i in liked_index_list:
				continue
			random_item = Item.objects.only('item_type', 'color', 'fit', 'occasion', 'brand', 'pattern', 'fabric', 'length').filter(id=i).values_list('item_type', 'color', 'fit', 'occasion', 'brand', 'pattern', 'fabric', 'length').first()		
			random_items.append(random_item)

		try:
			for i,pk in zip(range(len(random_items)),pks):
				if pk in liked_index_list:
					continue
				#random_item = Item.objects.only('item_type', 'color', 'fit', 'occasion', 'brand', 'pattern', 'fabric', 'length').filter(id=i).exclude(id__in=liked_index_list).values_list('item_type', 'color', 'fit', 'occasion', 'brand', 'pattern', 'fabric', 'length').first()
				if pk == 3647:
					print(random_items[i]) 
				#print(random_items[i])
				#print(upl)
				#print(pk)
				#print('------')
				#random_item = ','.join(map(str,random_item))
				for j in range(0,8):
					

					if random_items[i][j] in 'N/A' and upl[j] in 'N/A': 
						continue
					elif random_items[i][j] in upl[j]:
						#print(random_items[i][j])
						#print(upl[j])
						if column_mapping[pref] == j:
							top_val_1.append(2)
							#print(top_val_1)
							if pk == 3647:
								print(str(top_val_1)) 
						else:
							top_val_1.append(0.5)
							#print(top_val_1)
							if pk == 3647:
								print(str(top_val_1))

				top = sum(top_val_1)
				bottom = 11
				# print(top)
				# print(bottom)
				# print(top/bottom)
				# print(round((2*top)/bottom,3))
				if pk == 3647:
					print(str(top))
					print(str(bottom))
					print(str(top/bottom))
				dice_coe[str(pk)] = round((2*top)/bottom,3)
				top_val_1.clear()
				#print(dice_coe)
			


			desc_coe_dict = sorted(dice_coe, key = dice_coe.get, reverse = True)
			for value in desc_coe_dict:
				#print(dice_coe[value])
				#print(value)
				desc_coe_list.append(value)

			print(desc_coe_list[:11])
			for d in desc_coe_list[:11]:
				print(dice_coe[d])
		except:
			print('Exception occured')
			print(pk)
			print(i)
			traceback.print_exc()
		
		finally:
			connection.close()
			context = { 
				'desc_coe_list':desc_coe_list[:11],
			}
			return context
		context = { 
				'desc_coe_list':desc_coe_list[:11],
			}
		return context
		

	def get_preference_list(liked_index_list, pref):
		def item_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),item_type FROM (SELECT id,item_type, COUNT(item_type) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY item_type)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count
		def color_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),color FROM (SELECT id,color, COUNT(color) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY color)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count
		def fit_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),fit FROM (SELECT id,fit, COUNT(fit) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY fit)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count
		def occasion_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),occasion FROM (SELECT id,occasion, COUNT(occasion) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY occasion)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count
		def brand_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),brand FROM (SELECT id,brand, COUNT(brand) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY brand)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count
		def pattern_sql(liked_index_list):
			none_check = 'N/A'
			str11 = 'SELECT id,max(mycount),pattern FROM (SELECT id,pattern, COUNT(pattern) mycount FROM recommender_item where pattern is not' 
			str12 = "'"+none_check+"'"
			str13 = 'and'
			str14 = ' id in ('
			str15 = ','.join(map(str,liked_index_list))
			str16 = ') GROUP BY pattern)'
			q2 = str11 + str12 + str13 + str14 + str15 +str16
			count = Item.objects.raw(q2)

			return count
		def fabric_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),fabric FROM (SELECT id,fabric, COUNT(fabric) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY fabric)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count
		def length_sql(liked_index_list):
			str11 = 'SELECT id,max(mycount),length FROM (SELECT id,length, COUNT(length) mycount FROM recommender_item where id in ('
			str12 = ','.join(map(str,liked_index_list))
			str13 = ') GROUP BY length)'
			q2 = str11 + str12 + str13
			count = Item.objects.raw(q2)
			return count

		item_count = item_sql(liked_index_list)
		color_count = color_sql(liked_index_list)  
		fit_count = fit_sql(liked_index_list)
		occasion_count =  occasion_sql(liked_index_list)
		brand_count = brand_sql(liked_index_list)
		pattern_count = pattern_sql(liked_index_list)
		fabric_count = fabric_sql(liked_index_list)
		length_count = length_sql(liked_index_list)

		#print(item_count)
		user_preference_list = []
		for a,b,c,d,e,f,g,h in zip(item_count, color_count, fit_count, occasion_count, brand_count, pattern_count, fabric_count, length_count):
			user_preference_list.extend([a.item_type, b.color, c.fit, d.occasion, e.brand, f.pattern, g.fabric, h.length ])
		#print(user_preference_list)
		return get_sim(pref, liked_index_list, user_preference_list)

	def liked_item_ids(pref):
		def liked_ids_sql():
			with connection.cursor() as cursor:
				cursor.execute('select id from recommender_item where id in (select item_id from recommender_item_likes where user_id = %s)', [request.user.id])
				row = cursor.fetchall()
				return row
		liked_index_list = liked_ids_sql()
		liked_index_list = [e for l in liked_index_list for e in l]
		#print(liked_index_list)
		return get_preference_list(liked_index_list, pref)

	def get_user_pref():
		if request.method == 'POST':
			pref = request.POST.get('preference')
			pref = pref.strip()
			#print(pref)
			return liked_item_ids(pref)

	def get_preference_list_single(pref, pref_index_list):
		column_mapping = {'item_type': 0, 'color': 1, 'fit': 2, 'occasion': 3, 'brand': 4, 'pattern': 5, 'fabric':6, 'length': 7}
		#Get preference index and actual prefernce choice of user (i.e if user enters color, then pref_index = 4 and value will be the value for color in preference list)
		for key in column_mapping.keys():
			if pref in key:
				pref_index = column_mapping[key]
				pref_choice = pref_list[pref_index]
				#print(pref_index)
				#print(type(pref_choice))
				break

		#Retrieve ids of liked items
		

		matching_pref_list = []

		#Retrieve all items that match entered preference
		user_pref = pref
		#print(type(request.user.id))
		user_pref_list = []
	
		str1 = 'select id FROM recommender_item WHERE id in (select item_id from recommender_item_likes where user_id ='
		str2 = str(request.user.id)
		str3 = ') and '
		str4 = user_pref
		str5 = ' = '
		str6 = "'"+pref_choice+"'"
		q = str1 + str2+ str3 + str4 + str5 + str6
		#print(q)
		user_items = Item.objects.raw(q)
		for item in user_items:
			user_pref_list.append(item.id)
		#print(user_pref_list)
		item_type_new_count = []
		item_type_new = []
		for ids in user_pref_list:
			item_type_new_count.append(Item.objects.only('item_type', 'color', 'fit', 'occasion', 'brand', 'pattern', 'fabric', 'length').filter(id = ids).values_list('item_type', 'color', 'fit', 'occasion', 'brand', 'pattern', 'fabric', 'length'))
		
		#print(item_type_new_count)
		for item in item_type_new_count:
			item_type_new.append(item[0])
		

	'''context = {
		'pref' : pref,
		'item_type_count': item_type_count,
		'color_count': color_count,
		'fit_count': fit_count,
		'occasion_count': occasion_count,
		'brand_count': brand_count,
		'pattern_count': pattern_count,
		'fabric_count': fabric_count,
		'length_count': length_count,
	}'''
	return render(request, template_name, context = get_user_pref())
		
def ItemLikeToggleView(request):
	#item = get_object_or_404(Item, id = request.POST.get('item_id'))
	item = get_object_or_404(Item, id = request.POST.get('id'))
	is_liked = False
	if item.likes.filter(id = request.user.id).exists():
		item.likes.remove(request.user)
		is_liked = False
	else:
		item.likes.add(request.user)
		is_liked = True
	context = {
		'item': item,
		'is_liked': is_liked,
		'total_likes': item.get_total_likes(),
	}
	if request.is_ajax():
		html = render_to_string('recommender/like_section.html', context, request = request)
		return JsonResponse({'form': html})

def ItemLikeAllToggleView(request, pk):
	item = get_object_or_404(Item, id = request.POST.get('id'))
	is_liked = False
	if item.likes.filter(id = request.user.id).exists():
		item.likes.remove(request.user)
		is_liked = False
	else:
		item.likes.add(request.user)
		is_liked = True
	context = {
		'item': item,
		'is_liked': is_liked,
		'total_likes': item.get_total_likes(),
	}
	if request.is_ajax():
		html = render_to_string('recommender/like_section.html', context, request = request)
		return JsonResponse({'form': html})
	

def AllLikedItemsView(request, pk):
	def liked_item_id():
		with connection.cursor() as cursor:
			cursor.execute('select image_URL from recommender_item where id in (select item_id from recommender_item_likes where user_id = %s)', [request.user.id])
			row = cursor.fetchall()
			return row
	template_name = 'recommender/all_liked.html'
	item = liked_item_id()
	#print(item)
	context = {
		'likes': item,
	}
	return render(request, template_name, context = context)

class ItemsAllView(generic.ListView):
	template_name = 'recommender/all_items.html'
	paginate_by = 20
	def get_queryset(self):
		return Item.objects.all().order_by('likes')[:50]

def ItemDetailView(request, pk):
	template_name = 'recommender/item_detail.html'
	paginate_by = 10
	item = get_object_or_404(Item, pk = pk)
	is_liked = False
	if item.likes.filter(id = request.user.id).exists():
		is_liked = True
	context = {

		'item': item,
		'is_liked': is_liked,
		'total_likes': item.get_total_likes(),
	}
	return render(request, template_name, context = context)

