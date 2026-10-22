variable "name_prefix" {
  description = "Globally unique lowercase prefix for demo Azure resources."
  type        = string
  default     = "swiftpaydemo"
  validation {
    condition     = can(regex("^[a-z0-9]{5,12}$", var.name_prefix))
    error_message = "Use 5-12 lowercase letters or digits."
  }
}

variable "location" {
  description = "Azure region for the illustrative deployment."
  type        = string
  default     = "eastus"
}

variable "node_vm_size" {
  description = "AKS system node VM size; review regional availability and cost."
  type        = string
  default     = "Standard_D2s_v5"
}

variable "tags" {
  description = "Resource tags."
  type        = map(string)
  default = {
    project     = "swift-payments-demo"
    environment = "demo"
    data-class  = "synthetic-only"
  }
}
