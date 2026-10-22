(function () {
  "use strict";
  angular.module("paymentsDemo", []).controller("PaymentsController", function () {
    var vm = this;
    vm.payments = [];
    vm.refresh = function () {
      vm.payments = [
        { reference: "DEMO-001", amount: "EUR 125.00", country: "DE", state: "PREVIEW ONLY" },
        { reference: "DEMO-002", amount: "USD 42.50", country: "US", state: "MANUAL REVIEW DEMO" },
        { reference: "DEMO-003", amount: "GBP 88.10", country: "GB", state: "PREVIEW ONLY" }
      ];
      vm.reviewCount = 1;
    };
    vm.refresh();
  });
}());
