/* this component is responsible of rendering the side bar of the page */

Vue.component('shop-left', {
   
    template: `
        
    `,

    data: function(){
        return {
            collections: [],
            selectedCollection: null
        }
    }
});


var shopLeftApp = new Vue({
    el: '#shopLeftApp'
})