new Vue({
    el: '#employeeApp',
    delimiters:['[[',']]'],
    data: {

      selectedEmployee:null,
    }
    ,
    methods: {
      selectEmployee: function(employee) {
        this.selectedEmployee = employee;
      }
    }
  })
new Vue({
    el: '#locationApp',
    delimiters:['[[',']]'],
    data: {

      selectedLocation:null,
    }
    ,
    methods: {
      selectLocation: function(location) {
        this.selectedLocation = location;
      }
    }
  })