/*
 Models
 */

App.OrderItem = DS.Model.extend({
    url: 'fund/orders/:order_id/items',

    // Model fields
    // FIXME Make the drf2 serializer use the id (or slug) to serialize DS.belongsTo.
    //       This will enable us to remove the project_slug field.
    project: DS.belongsTo('App.Project'),
    project_slug: DS.attr('string'),
    amount: DS.attr('number'),
    status: DS.attr('string'),
    type: DS.attr('string')
});


App.CurrentOrderItem = DS.Model.extend({
    url: 'fund/orders/current/items'
});


App.LatestDonation = App.OrderItem.extend({
    url: 'fund/orders/latest/donations'
});

App.CurrentDonation = App.OrderItem.extend({
    url: 'fund/orders/current/donations'
});



App.CurrentVoucher = App.OrderItem.extend({
    url: 'fund/orders/current/vouchers'
});


App.PaymentInfo = DS.Model.extend({
    url: 'fund/paymentinfo',
    payment_method: DS.attr('number'),
    amount: DS.attr('number'),
    firstName: DS.attr('string'),
    lastName: DS.attr('string'),
    address: DS.attr('string'),
    city: DS.attr('string'),
    country: DS.attr('string'),
    zipCode: DS.attr('string'),
    payment_url: DS.attr('string')
});


App.Payment = DS.Model.extend({
    url: 'fund/payments',
    payment_method: DS.attr('number'),
    amount: DS.attr('number'),
    status: DS.attr('string')
});


/*
 Controllers
 */

App.CurrentOrderItemListController = Em.ArrayController.extend({

    deleteOrderItem: function(donation) {
        var transaction = App.store.transaction();
        transaction.add(donation);
        donation.deleteRecord();
        transaction.commit();
    }

});


// TODO: Do we want to use this?
App.CurrentOrderController = Em.ObjectController.extend({

});


// TODO: Do we want to use this?
App.PaymentInfoController = Em.ObjectController.extend({

});

App.FinalOrderItemListController = Em.ArrayController.extend({
});


/*
 Views
 */

App.CurrentOrderView = Em.View.extend({
    templateName: 'currentorder'
});


App.CurrentOrderItemListView = Em.View.extend({
    templateName: 'currentorderitem_form',
    tagName: 'form'
});


App.FinalOrderItemListView = Em.View.extend({
    templateName: 'final_order_item_list',
    tagName: 'div'
});


App.OrderPaymentView = Em.View.extend({
    tagName: 'form',
    templateName: 'order_payment'
});


App.PaymentInfoView = Em.View.extend({
    tagName: 'form',
    templateName: 'payment_info'
});
