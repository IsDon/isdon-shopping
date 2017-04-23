#Shopping Cart App Documentation:

##Assumptions:

- Adding multiples of special_qty will apply discount across each quantity
- User / Session will use last "cart" for user (or session) - Loading another cart by id_hash will save into a new "latest" for logged in user
- Assuming prices from json service may change, but implementation not fully implemented - notes in code and below will refer to this
- App currently passes json product list from app to server (This needs to happen on server, with information passing back to frontend apps only)
- Items are only purchase-able in int (multiples of 1) - adding decimal amounts such as per kilo etc will required adjustments, including especially the price calculation which assumes ints in modulus calculation
- Shopping List and Cart are both sorted alphabetically

##Usage:

- Clicking Item name or single price will add 1 to cart
- Clicking Special quantity or price will add special qty to cart  (could be made to add up to next multiple of special qty, but seemed counter-intuitive)
- Cart will display items and quantity for order
- Cart will display total price for current quantities
- Clicking remove button on Cart row will remove the item from the cart (entire quantity)
- Cart is updated after the server saves quantity updates

##Other things to be aware of:

- Implementation does not include checks for multiple-clicks on click events before UI updates. Usage should be tested to determine if this is an issue
- Cart app doesn't handle removal of whole cart (clear) or raising/lowering of item counts individually from cart UI at present
- Errors from AJAX are not giving feedback in the UI - this should be added

##Taking it further:

- Next stage is definitely adding suite of unit tests to cover:
	- models
	- CRUD operations API
	- permissions* (and remove .IsAny from REST permissions in settings.py)
- Add basic functionality tests:
	- add items to new cart
	- clear cart
	- refresh page, still have cart
	- logout - lose cart*
* = functionality not implemented in current release.
- Users' shopping carts should be stored beyond just using 'latest', with id_hash as a url link (prices at time should be compared to a look up on stored shopping list data, also to be kept as historical dataset - with warning if prices have changed)
- Currently the shopping list data is passed to the server for updates from the user browser (very unsecure, bad practice, etc) - The shopping list should be updated at the server end with a server-side call to the product list url instead.
- Allow interface pattern on Buy operation with non-empty cart to send cart to new API resource with purchase options and rest of procedure.
- Shop owner App would allow for changing resource location, reviewing current open carts, viewing ordered carts.