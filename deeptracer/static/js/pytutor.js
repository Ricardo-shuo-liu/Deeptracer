/**
 * pytutor.js - PyTutor iframe 编码 + 渲染逻辑
 * 功能：
 * 1. 对Python代码进行URL编码
 * 2. 构造Python Tutor的iframe URL
 * 3. 生成完整的可视化界面
 */

// 生成Python Tutor iframe URL
function generatePyTutorUrl(code) {
    // 1. 清理代码（去掉首尾空格）
    const cleanedCode = code.trim();
    
    // 2. 严格URL编码（解决特殊字符、换行符问题）
    const encodedCode = encodeURIComponent(cleanedCode);
    
    // 3. 构造Python Tutor原生完整URL（还原所有核心参数）
    const pytutorUrl = `https://pythontutor.com/iframe-embed.html#` +
        `code=${encodedCode}&` +          // 编码后的代码
        `origin=opt-frontend.js&` +      // 来源标识（必须）
        `cumulative=false&` +            // 不累计显示变量（原生效果）
        `heapPrimitives=true&` +         // 基础类型放入堆区（显示箭头）
        `textReferences=false&` +        // 禁用文本引用（显示图形化箭头）
        `py=311&` +                      // 指定Python 3.11（最新稳定版）
        `rawInputLstJSON=%5B%5D&` +      // 无输入
        `curInstr=0&` +                  // 从第0步开始
        `verticalStack=false&` +         // 水平布局（原生）
        `hideVars=false&` +              // 显示变量（关键）
        `theme=plain`;                   // 原生主题
    
    return pytutorUrl;
}