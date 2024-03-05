import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WordContextComponent } from './word-context/word-context.component';

// Define routes
const routes: Routes = [
  { path: 'word-context', component: WordContextComponent },
  { path: '', redirectTo: '/word-context', pathMatch: 'full' }, // Redirect default route to your component
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }