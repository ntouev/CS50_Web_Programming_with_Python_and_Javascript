document.addEventListener('DOMContentLoaded', () => {
    //reset Topping to none checked
    document.querySelectorAll('.check_class').forEach( item => {
        item.checked = false;
    });

    show('regular');

    let previous_food_type = 'regular';
    let current_food_type = '';

    //What happens when I click a food_type on the dropdown
    document.querySelector('#food_selection_form').onchange = () => {
        current_food_type = document.querySelector('#food_type').value;
        hide(previous_food_type);
        show(current_food_type);

        if ((current_food_type == 'regular') || (current_food_type =='sicilian')) {
            show('size_form');
            show('topping_form');
        } else {
            hide('topping_form');
        }

        previous_food_type = current_food_type;
        return false;
    };

    //with submittion to the shopping cart retrieve the following values
    document.querySelector('#submit_to_basket').onclick = () => {
        food_type = document.querySelector('#food_type').value;
        food_type_type = document.querySelector('#' + CSS.escape(food_type) + '_type').value;
        if (document.querySelector('#small').checked) {var size = 'small';}
        if (document.querySelector('#large').checked) {var size = 'large';}

        //topping_array is an array with the checked toppings
        var toppings = document.forms[6]; //toppings is the 6th form
        var topping_array=[];
        for (i=0; i<toppings.length; i++){
            if (toppings[i].checked){
                topping_array.push(toppings[i].value);
            }
        }

        //reset Topping to none checked since an order has been submitted to shopping cart
        document.querySelectorAll('.check_class').forEach( item => {
            item.checked = false;
        });

        return false;
    };
});

//function to show html forms
function show(food_type) {
    document.querySelector('#' + CSS.escape(food_type)).style.visibility = 'visible';
    document.querySelector('#' + CSS.escape(food_type)).style.display = 'block';
}

//function to hide html forms
function hide(food_type) {
    if (food_type === null) {

    } else {
        document.querySelector('#' + CSS.escape(food_type)).style.visibility = 'hidden';
        document.querySelector('#' + CSS.escape(food_type)).style.display = 'none';
    }
}

