import '../css/base.css'
import '../css/lists.css'
 
var React = require('react')
var ReactDOM = require('react-dom')
 
var MAPPING = [{
		'uri':'/cart/',
		'remove':false,
		'add':'cart/add/',
		'header':'Shopping List',
		'fields':['name','unit_price','special_qty','special_price']
	},{
		'uri':'/cart/',
		'remove':'cart/remove/',
		'add':false,
		'header':'Cart',
		'fields':['item__name','quantity','qu_price']
	}];
  
class DjangoCSRFToken extends React.Component {
  render() {
    var csrfToken = Django.csrf_token();
    return React.DOM.input(
      {type:"hidden", name:"csrfmiddlewaretoken", value:csrfToken}
    );
  }
}

class ButtonRemoveItem extends React.Component {
	render() {
		return (
			<button onClick={this.props.removeFn}>x</button>
		)
	} 
}


class ItemRow extends React.Component {
	constructor(props) {
		super(props);
		this.fields = this.props.mapped['fields'];
	}

	render() {
		let item = this.props.obj;
		let clickSingle, clickSpecial;
		var top = this.props.top;
		if(this.props.mapped['add']) {
			clickSingle = top.addItem.bind(
				top, 
				this.props.mapped['add'],
				item.id, 
				1
			);
			clickSpecial = top.addItem.bind(
				top, 
				this.props.mapped['add'],
				item.id, 
				item.special_qty
			);
		}
		let item_heading;
		item_heading = this.fields.map(function(prop, index){
			let clickEvent;
			if(index<2) {
				clickEvent = clickSingle
			} else {
				clickEvent = clickSpecial
			}
			if (!(prop.slice(-4)==='name' || item[prop]>0)) {		//0 or null
				return (
					<span key={index}></span>
				)
			} else if (prop.slice(-6) == '_price') {
				return (
					<span key={index} onClick={clickEvent}>
						{'$'+item[prop]}
					</span>
				);
			} else {
				return (
					<span key={index} onClick={clickEvent}>
						{item[prop]}
					</span>
				);
			}
		})
		let remove_btn;
		if(this.props.mapped['remove']) {
			remove_btn = (
				<ButtonRemoveItem 
					id={item.id} 
					removeFn={this.props.top.removeItem.bind(
						this.props.top, 
						item.id_link, 
						this.props.mapped['remove']
					)} 
				/>
			);
		}
		return (
        	<li key={item.id.toString()} >
        		<h3>{item_heading}</h3>
        		{remove_btn}
        	</li>
		)
	}
}

class ItemNodes extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		var top = this.props.top;	
		var uri = this.props.uri;
		var mapped = this.props.mapped;
        var perItemNodes = null;
        if(this.props.items) {
        	console.log(this.props.items);
        	perItemNodes = this.props.items.map(function(item){
        		//removeFn={top.removeItem.bind(top, item.id, MAPPING['uri'])}
	        	return (
	        		<ItemRow 
		        		key={item.id.toString()} 
		        		obj={item} 
		        		top={top} 
		        		mapped={mapped}
		        	/>
	        	)
	        })
    	}
        return (
            <div className="border">
                <div className="list">
	                <ul>
	                	<li className="header">
			                <h4>{mapped["header"]}</h4>
	               		</li>
        				{perItemNodes}
	                </ul>
	            </div>
            </div>
        )
	}
}




class ShoppingList extends React.Component {
	constructor(props) {
		super(props);
		this.state = { 
			data:[]
		}
		//bind functions in constructor where required:
		this.loadDataFromServer = this.loadDataFromServer.bind(this);
	}

    loadDataFromServer() {
        $.ajax({
            url: this.props.url,
            type: 'get',
            datatype: 'json',
            cache: false,
            success: function(data_api) {
            	var csrfToken = Django.csrf_token();
            	data_api["csrfmiddlewaretoken"]=csrfToken;
            	//send ajax to server, update ShoppingList and bind returned latest ShoppingList with id's to this.state
                $.ajax({
                	url: '/shopping/update/',
                	type: 'post',
                	contentType:"application/json",
                	data: JSON.stringify(data_api),
                	success: function(data_returned) {
                		if(typeof(data_returned.error == 'undefined')) {
                			this.setState({data: data_returned})
                		}
                	}.bind(this)
                })
            }.bind(this)
        })
    }

    addItem(uri, id, amount, e) {
    	e.preventDefault();
    	console.log(uri);
    	console.log(id);
    	console.log(amount);

    	//sanity check:
    	if(! amount>0) {
    		return;
    	}

    	// TODO: Highlight (or fade-out) row in checkout if item already in checkout to show data changing

    	$.ajax({
    		url: '/cart/add/' + id + '/' + amount + '/',
    		type: 'get',
		//	data: (using url params)
    		datatype: 'json',
    		cache: false,
    		success: function(data) {
    		//	this.loadDataFromServer();
    		//	update Cart with data       TODO
    			//console.log(this.props.parentApp.cart);
                if(typeof(data.error == 'undefined')) {
    				this.props.parentApp.cart.setState({data:data});
    			}
    		}.bind(this)
    	})
    }

    componentDidMount() {
        this.loadDataFromServer();
//SETUP: If we want to handle auto-refresh, enable polling and pass pollInterval from ReactDOM init:
        // setInterval(this.loadListFromServer, 
        //             this.props.pollInterval)
    }

    render() {
        return (
        	<ItemNodes items={this.state.data} top={this} pk={-1} mapped={MAPPING[0]} />
        )
    }
}


class ShoppingCart extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			data:[]
		}
		//bind functions in constructor where required:
		this.loadDataFromServer = this.loadDataFromServer.bind(this);
	}

    loadDataFromServer() {
        $.ajax({
            url: this.props.url,
            type: 'get',
            datatype: 'json',
            cache: false,
            success: function(data) {
                if(typeof(data.error == 'undefined')) {
              		this.setState({data: data});
              	}
            }.bind(this)
        })
    }

    addItem(uri, e) {
    	e.preventDefault();
    	var form = e.target;

    	$.ajax({
    		url: this.props.url + uri + '/',
    		type: 'get',
    		datatype: 'json',
    		cache: false,
    		success: function(data) {
    			this.loadDataFromServer();
    		}.bind(this)
    	})
    }

    removeItem(id, uri, e) {
    	console.log('removing item ' + uri + ' @' + id);
    	e.preventDefault();
    	var csrfToken = Django.csrf_token();
    	var data_csrf = {};
        data_csrf["csrfmiddlewaretoken"]=csrfToken;
    	$.ajax({
    		url: uri + id + '/',
    		type: 'post',
            contentType:"application/json",
    		data: JSON.stringify(data_csrf),
    		cache: false,
    		success: function(data) {
                if(typeof(data.error == 'undefined')) {
              		this.setState({data: data});
              	}
    		}.bind(this)
    	})
    }

    componentDidMount() {
        this.loadDataFromServer();
//SETUP: If we want to handle auto-refresh, enable polling and pass pollInterval from ReactDOM init:
        // setInterval(this.loadListFromServer, 
        //             this.props.pollInterval)
    }

    render() {
        return (
        	<ItemNodes items={this.state.data} top={this} pk={-1} mapped={MAPPING[1]} />
        )
    }
}

class ShoppingApp extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div>
				<div id="ShoppingAppContainer" className="appcontainer">
					<ShoppingList url='https://api.myjson.com/bins/gx6vz' parentApp={this} />
				</div>
				<div id="CartContainer" className="appcontainer">
					<ShoppingCart url='/cart/latest/' ref={(app) => { this.cart = app; }} />
				</div>
			</div>
		)
	}
}

//Parent app - render to DOM via React:
 ReactDOM.render(<ShoppingApp />, 
     document.getElementById('ShoppingAppsContainer'))