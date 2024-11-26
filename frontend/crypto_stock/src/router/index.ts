import { createRouter, createWebHistory } from 'vue-router'
import HomeComponent from '../components/HomeComponent.vue'
import BuySellComponent from '../components/Stocks/BuySellComponent.vue'
import ForCompaniesComponent from '../components/ForCompaniesComponent.vue'
import LoginPage from '../components/LoginPage.vue'
import StocksPage from '../components/StocksPage.vue'
import CompanyDetail from '../components/Stocks/CompanyDetail.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeComponent },
  { path: '/buy-sell', name: 'BuySell', component: BuySellComponent },
  { path: '/for-companies', name: 'ForCompanies', component: ForCompaniesComponent },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/company/:id', name: 'companyDetail', component: CompanyDetail, props: true },
  { path: '/stocks', name: 'StocksPage', component: StocksPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;