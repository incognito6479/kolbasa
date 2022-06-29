from .models import MovementItem, Movement
from warehouse.models import WarehouseProduct
from django.db.models import Sum


def add_movement_item(request, kwargs):
	movement_id = int(kwargs['pk'])
	product_id = request.POST.get('product')
	count = float(request.POST.get('count'))
	price = int(request.POST.get('price'))
	total = count * price
	obj, created = MovementItem.objects.get_or_create(
											movement_id=movement_id,
											warehouse_product_id=product_id,
											defaults={
												'count': count,
												'price': price,
												'total': total,
											}
										)
	if not created:
		obj.count = count
		obj.price = price
		obj.total = obj.count * obj.price
		obj.save()
	total_item_sum = MovementItem.objects.filter(movement_id=movement_id).aggregate(Sum('total'))
	Movement.objects.filter(id=movement_id).update(total=total_item_sum.get('total__sum', 0))
	return 1


def change_movement_status(request, kwargs):
	status = request.POST.get('change_status')
	movement_instance = Movement.objects.get(id=kwargs['pk'])
	movement_items = MovementItem.objects.filter(movement=movement_instance)
	if status == 'completed':
		for movement_item in movement_items:
			warehouse_product_to_move = WarehouseProduct.objects.get(
									warehouse_id=movement_item.movement.from_warehouse_id,
									product_id=movement_item.warehouse_product.product_id,
												)
			warehouse_product_to_move.count -= movement_item.count
			warehouse_product_to_move.save()

			obj, created = WarehouseProduct.objects.get_or_create(
												warehouse_id=movement_item.movement.to_warehouse_id,
												product_id=movement_item.warehouse_product.product_id,
												defaults={
													'count': movement_item.count,
													'self_price': movement_item.price,
													}
												)  # warehouse_product_to_add
			if not created:
				obj.count += movement_item.count
				obj.self_price = movement_item.price
				obj.save()
	if status == 'rejected' and movement_instance.status == 'completed':
		for movement_item in movement_items:
			warehouse_product_to_return = WarehouseProduct.objects.get(
									warehouse_id=movement_item.movement.to_warehouse_id,
									product_id=movement_item.warehouse_product.product_id,
												)
			warehouse_product_to_return.count -= movement_item.count
			warehouse_product_to_return.save()

			obj, created = WarehouseProduct.objects.get_or_create(
												warehouse_id=movement_item.movement.from_warehouse_id,
												product_id=movement_item.warehouse_product.product_id,
												defaults={
													'count': movement_item.count,
													'self_price': movement_item.price,
													}
												)  # warehouse_product_to_return
			if not created:
				obj.count += movement_item.count
				obj.self_price = movement_item.price
				obj.save()
	movement_instance.status = status
	movement_instance.save()
	return 1 


def delete_movement_item(request, kwargs):
	product_id = int(request.POST.get('product'))
	MovementItem.objects.filter(id=product_id, movement_id=kwargs['pk']).delete()
	total_item_sum = MovementItem.objects.filter(movement_id=kwargs['pk']).aggregate(Sum('total'))
	if total_item_sum.get('total__sum'):
		Movement.objects.filter(id=kwargs['pk']).update(total=total_item_sum.get('total__sum', 0))
	else:
		Movement.objects.filter(id=kwargs['pk']).update(total=0)
	return 1
