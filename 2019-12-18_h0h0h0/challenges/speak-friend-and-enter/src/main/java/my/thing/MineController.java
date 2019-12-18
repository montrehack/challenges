package my.thing;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ExceptionHandler;

import org.springframework.expression.Expression;  
import org.springframework.expression.ExpressionParser;  
import org.springframework.expression.spel.standard.SpelExpression;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.SpelNode;
import org.springframework.expression.spel.ast.*;

import java.util.List;
import java.util.ArrayList;

@Controller
public class MineController {
    ArrayList<Class> GOOD_SPEL = new ArrayList<Class>(List.of(StringLiteral.class, MethodReference.class, CompoundExpression.class, Identifier.class, QualifiedIdentifier.class));

    @GetMapping({"/"})
    public String hello() {
        return "hello";
    }

    @GetMapping({"/enter"})
    public String enter(Model model,
                        @RequestParam(value="spel", required=false, defaultValue="'Friend'") String spel) throws Exception {
        ExpressionParser parser = new SpelExpressionParser();
        Expression exp = parser.parseExpression(spel);

        SpelExpression sExp = (SpelExpression) exp;
        SpelNode root = sExp.getAST();
        ArrayList<SpelNode> nodes = getChilds(root);
        blackSpel(nodes);

        Object message = exp.getValue();

        model.addAttribute("message", message.toString());

        return "spel";
    }

    @ExceptionHandler(Exception.class)
    public String error(Model model, Exception ex) {
        model.addAttribute("exception", ex);
        return "error";
    }

    private ArrayList<SpelNode> getChilds(SpelNode node) {
        ArrayList<SpelNode> childs = new ArrayList<SpelNode>();

        for(int i = 0; i < node.getChildCount(); i++){
            childs.addAll(getChilds(node.getChild(i)));
        }

        childs.add(node);

        return childs;
    }

    private void blackSpel(ArrayList<SpelNode> nodes) throws Exception {

        for(SpelNode node:nodes) {
            if(GOOD_SPEL.indexOf(node.getClass()) == -1){
                String className = node.getClass().getName();
                throw new Exception("The balrog sensed your " + className);
            }
        }

    }
}
