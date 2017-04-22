Shopping Cart App Documentation:

Assumptions:

- Adding multiples of special_qty will apply discount across each quantity
- User / Session will use last "cart" for user (or session) - Loading another cart by id_hash will save into a new "latest" for logged in user
- Assuming prices from json service may change, but implementation not fully implemented - notes in code and below will refer to this
- Items are only purchase-able in int (multiples of 1) - adding decimal amounts such as per kilo etc will required adjustments, including especially the price calculation which assumes ints in modulus calculation
- Shopping List and Cart are both sorted alphabetically

Usage:

- Clicking Item name or single price will add 1 to cart
- Clicking Special quantity or price will add special qty to cart
- Cart will display items and quantity for order
- Cart will display total price for current quantities
- Clicking remove button on Cart row will remove the item from the cart (entire quantity)
- Cart is updated after the server saves quantity updates

Other things to be aware of:

- Implementation does not include checks for multiple-clicks on click events before UI updates. Usage should be tested to determine if this is an issue
- Cart app doesn't handle removal of whole cart (clear) or raising/lowering of item counts individually from cart UI at present
- Errors from AJAX are not giving feedback in the UI - this should be added

Taking it further:

- Users' shopping carts should be stored beyond just using 'latest', with id_hash as a url link (prices at time should be compared to a look up on stored shopping list data, also to be kept as historical dataset - with warning if prices have changed)
