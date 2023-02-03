package model;
import static interface_grafica.Carrinho.listadejogos;
import static interface_grafica.Carrinho.selExc;
import static interface_grafica.Carrinho.txtNome1;
import static interface_grafica.Carrinho.txtNome10;
import static interface_grafica.Carrinho.txtNome11;
import static interface_grafica.Carrinho.txtNome2;
import static interface_grafica.Carrinho.txtNome3;
import static interface_grafica.Carrinho.txtNome4;
import static interface_grafica.Carrinho.txtNome5;
import static interface_grafica.Carrinho.txtNome7;
import static interface_grafica.Carrinho.txtNome8;
import static interface_grafica.Carrinho.txtNome9;
import static interface_grafica.Carrinho.txtSubtotal;
import static interface_grafica.Carrinho.txtValor1;
import static interface_grafica.Carrinho.txtValor10;
import static interface_grafica.Carrinho.txtValor11;
import static interface_grafica.Carrinho.txtValor2;
import static interface_grafica.Carrinho.txtValor3;
import static interface_grafica.Carrinho.txtValor4;
import static interface_grafica.Carrinho.txtValor5;
import static interface_grafica.Carrinho.txtValor7;
import static interface_grafica.Carrinho.txtValor8;
import static interface_grafica.Carrinho.txtValor9;

import java.util.ArrayList;

public class CarrinhoA{
    
public static boolean verifica(int x){ /*vê quantos elementos tem na arraylist*/
    if(listadejogos.size()>x){
        return true;
    }else{
        return false;
    }
}

   public static void RemoverdoCarrinho(){
        String escolha= selExc.getSelectedItem().toString(); 
        /*verifica a escolha e o numero de elementos*/
        
       if(escolha.equals("Jogo 1")&& listadejogos.size()>=1){
            listadejogos.remove(0);
        }else if (escolha.equals("Jogo 2")&& listadejogos.size()>=2){
            listadejogos.remove(1);
        }else if(escolha.equals("Jogo 3")&& listadejogos.size()>=3){
            listadejogos.remove(2);
        }else if(escolha.equals("Jogo 4")&& listadejogos.size()>=4){
            listadejogos.remove(3);
        }
        
        else if(escolha.equals("Jogo 5")&& listadejogos.size()>=5){
            listadejogos.remove(4);
        }
        else if(escolha.equals("Jogo 6")&& listadejogos.size()>=6){
            listadejogos.remove(5);
        }
        else if(escolha.equals("Jogo 7")&& listadejogos.size()>=7){
            listadejogos.remove(6);
        }
        else if(escolha.equals("Jogo 8")&& listadejogos.size()>=8){
            listadejogos.remove(7);
        }
         else if(escolha.equals("Jogo 9")&& listadejogos.size()>=8){
            listadejogos.remove(8);
        }
         else if(escolha.equals("Jogo 10")&& listadejogos.size()>=8){
            listadejogos.remove(9);
        }
   }
 
   public static void MostrarnoCarrinho(){
        float subt = 0f;
        txtSubtotal.setText( Float.toString(subt));/*variavel q calcula o preço total*/

        if(listadejogos.isEmpty()){ /*pega o valor e o nome de acordo com a quantidade de elementos*/

        }else{txtNome1.setText(listadejogos.get(0).getNome());
            txtValor1.setText(Float.toString(listadejogos.get(0).getValor()));
            subt = listadejogos.get(0).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor1.setVisible(true);
        }

        if(verifica(1)){
            txtNome2.setText(listadejogos.get(1).getNome());
            txtValor2.setText(Float.toString(listadejogos.get(1).getValor()));
            subt = subt + listadejogos.get(1).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f); /*usando o método Math.round para arredondar o valor da variável para 2 casas decimais*/
            txtSubtotal.setText(Float.toString(subt));
            txtValor2.setVisible(true);
        }

        if(verifica(2)){
            txtNome3.setText(listadejogos.get(2).getNome());
            txtValor3.setText(Float.toString(listadejogos.get(2).getValor()));
            subt = subt + listadejogos.get(2).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor3.setVisible(true);
        }

        if(verifica(3)){
            txtNome4.setText(listadejogos.get(3).getNome());
            txtValor4.setText(Float.toString(listadejogos.get(3).getValor()));
            subt = subt + listadejogos.get(3).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor4.setVisible(true);
        }
        
        if(verifica(4)){
            txtNome5.setText(listadejogos.get(4).getNome());
            txtValor5.setText(Float.toString(listadejogos.get(4).getValor()));
            subt = subt + listadejogos.get(4).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor5.setVisible(true);
        }
        
        if(verifica(5)){
            txtNome7.setText(listadejogos.get(5).getNome());
            txtValor7.setText(Float.toString(listadejogos.get(5).getValor()));
            subt = subt + listadejogos.get(5).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor7.setVisible(true);
        }
        
        if(verifica(6)){
            txtNome8.setText(listadejogos.get(6).getNome());
            txtValor8.setText(Float.toString(listadejogos.get(6).getValor()));
            subt = subt + listadejogos.get(6).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor8.setVisible(true);
        }
        
        if(verifica(7)){
            txtNome9.setText(listadejogos.get(7).getNome());
            txtValor9.setText(Float.toString(listadejogos.get(7).getValor()));
            subt = subt + listadejogos.get(7).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor9.setVisible(true);
            
        }
        
        if(verifica(8)){
            txtNome10.setText(listadejogos.get(8).getNome());
            txtValor10.setText(Float.toString(listadejogos.get(8).getValor()));
            subt = subt + listadejogos.get(8).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor10.setVisible(true);
        }
        
        if(verifica(9)){
            txtNome11.setText(listadejogos.get(9).getNome());
            txtValor11.setText(Float.toString(listadejogos.get(9).getValor()));
            subt = subt + listadejogos.get(8).getValor();
            subt = (float) (Math.round(subt * 100f) / 100f);
            txtSubtotal.setText(Float.toString(subt));
            txtValor11.setVisible(true);
        }
   }    
}
