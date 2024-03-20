new_company_el = document.querySelector("#new-company")
new_company_trigger = document.querySelector(".new-company-trigger")
new_company_trigger_close = document.querySelector(".new-company-trigger-close")

new_company_trigger.addEventListener('click', ()=>{
	new_company_el.style.display = "grid"
	new_company_trigger_close.style.display = "block"
})
new_company_trigger_close.addEventListener('click', ()=>{
	new_company_el.style.display = 'none'
})