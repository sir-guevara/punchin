new Vue({
    el: '#employeeApp',
    delimiters:['[[',']]'],
    data: {

      selectedEmployee: null
    }
    ,
    methods: {
      selectEmployee: function(employee) {
        this.selectedEmployee = employee;
        console.log(this.selectedEmployee)
      }
    }
  })